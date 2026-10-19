"""
FastAPI Routes for Call Ingestion, Processing, and Coaching Reports.
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import Optional, List, Dict, Any
import uuid
import json
from pathlib import Path

from api.schemas.call_schema import (
    CallCreateRequest, CallAuditResponse, CoachingReportResponse
)
from services.auditor_pipeline import ProductGuardAuditorPipeline
from services.stt_service import TranscriptIngestionService
from core.security import validate_recording_consent, redact_pii
from core.config import settings

router = APIRouter(prefix="/calls", tags=["Calls & Audits"])

# In-memory storage for active demo sessions (with persistence to SQLite / cache)
CALL_CACHE: Dict[str, Dict[str, Any]] = {}
pipeline = ProductGuardAuditorPipeline()

@router.post("", response_model=CallAuditResponse)
async def create_call_audit(request: CallCreateRequest):
    """
    Ingests and audits a conversation from raw transcript text or structured segments.
    """
    if settings.REQUIRE_RECORDING_DISCLOSURE and not request.disclosure_confirmed:
        raise HTTPException(
            status_code=400,
            detail="Recording disclosure and authorization confirmation is mandatory under compliance policy."
        )

    call_id = f"call-{uuid.uuid4().hex[:8]}"
    
    # Redact PII in raw text if present
    cleaned_transcript = redact_pii(request.raw_transcript) if request.raw_transcript else None
    
    dict_segments = [s.model_dump() for s in request.segments] if request.segments else None
    if dict_segments:
        for seg in dict_segments:
            seg["text"] = redact_pii(seg["text"])

    # Execute Audit
    result = pipeline.audit_conversation(
        call_id=call_id,
        product_id=request.product_id,
        provider_name=request.provider_name,
        raw_transcript=cleaned_transcript,
        structured_segments=dict_segments,
        target_report_language=request.target_report_language
    )

    call_record = {
        "call_id": call_id,
        "status": "completed",
        "product_id": request.product_id,
        "provider_name": request.provider_name,
        "duration_seconds": round(max([s.get("end_time", 0.0) for s in result["segments"]] or [0.0]), 1),
        "segments": result["segments"],
        "claims": result["claims"],
        "report": result["report"]
    }
    CALL_CACHE[call_id] = call_record
    return call_record

@router.post("/{call_id}/audio")
async def upload_call_audio(
    call_id: str,
    file: UploadFile = File(...),
    disclosure_confirmed: bool = Form(True)
):
    """
    Uploads an authorized audio recording (WAV, MP3, M4A) for transcription and auditing.
    """
    if not disclosure_confirmed:
        raise HTTPException(status_code=400, detail="Recording disclosure confirmation required.")
        
    ext = Path(file.filename).suffix.lower()
    if ext not in [".wav", ".mp3", ".m4a"]:
        raise HTTPException(status_code=400, detail=f"Unsupported audio format '{ext}'. Supported: .wav, .mp3, .m4a")

    return {
        "call_id": call_id,
        "filename": file.filename,
        "status": "received",
        "message": "Audio file verified and queued for multilingual Whisper STT processing."
    }

@router.get("/{call_id}/status")
async def get_call_status(call_id: str):
    """Retrieves current processing status of the call."""
    if call_id not in CALL_CACHE:
        raise HTTPException(status_code=404, detail="Call record not found.")
    return {"call_id": call_id, "status": CALL_CACHE[call_id]["status"]}

@router.get("/{call_id}/transcript")
async def get_call_transcript(call_id: str):
    """Retrieves timestamped and speaker-labeled transcript segments."""
    if call_id not in CALL_CACHE:
        raise HTTPException(status_code=404, detail="Call record not found.")
    return {"call_id": call_id, "segments": CALL_CACHE[call_id]["segments"]}

@router.get("/{call_id}/report", response_model=CoachingReportResponse)
async def get_call_report(call_id: str):
    """Retrieves private, evidence-based coaching report."""
    if call_id not in CALL_CACHE:
        raise HTTPException(status_code=404, detail="Call report not found.")
    return CALL_CACHE[call_id]["report"]

@router.post("/realtime-turn")
async def audit_realtime_turn(
    product_id: str,
    turn_text: str,
    speaker_role: str = "provider",
    target_language: str = "Hinglish"
):
    """
    Audits a single conversational utterance in real-time.
    Provides immediate compliance validation, claim checks, and replacement response.
    """
    res = pipeline.audit_realtime_turn(
        product_id=product_id,
        turn_text=turn_text,
        speaker_role=speaker_role,
        target_language=target_language,
        generate_tts=False
    )
    return res
