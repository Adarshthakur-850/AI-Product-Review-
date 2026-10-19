"""
Pydantic schemas for Calls, Transcripts, Claims, and Coaching Reports.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class TranscriptSegmentSchema(BaseModel):
    speaker_role: str = Field(..., description="'customer' or 'provider'")
    start_time: float = 0.0
    end_time: float = 0.0
    text: str
    detected_language: Optional[str] = "en"
    language_label: Optional[str] = "English"
    confidence: float = 1.0
    topic_category: Optional[str] = None
    is_off_topic: bool = False

class CallCreateRequest(BaseModel):
    product_id: str
    provider_name: str
    customer_name: Optional[str] = "Customer"
    disclosure_confirmed: bool = True
    primary_language: str = "Hinglish"
    target_report_language: str = "Hinglish"
    raw_transcript: Optional[str] = None
    segments: Optional[List[TranscriptSegmentSchema]] = None

class ClaimSchema(BaseModel):
    original_statement: str
    timestamp: float
    category: str
    claim_text: str
    verification_status: str
    supporting_source: Optional[str] = None
    supporting_excerpt: Optional[str] = None
    explanation: Optional[str] = None
    corrected_text: Optional[str] = None
    confidence: float = 0.9

class CoachingReportResponse(BaseModel):
    call_id: str
    provider_name: str
    product_name: str
    overall_score: float
    tier: str
    breakdown: Dict[str, Any]
    deductions: List[Dict[str, Any]]
    summary: str
    customer_questions: List[str]
    features_discussed: List[str]
    effective_statements: List[str]
    off_topic_statements: List[Dict[str, Any]]
    suggested_replacements: List[Dict[str, Any]]
    action_plan: List[str]
    language_feedback: Optional[str] = None
    confidence_limitation_note: str

class CallAuditResponse(BaseModel):
    call_id: str
    status: str
    product_id: str
    provider_name: str
    duration_seconds: float
    segments: List[Dict[str, Any]]
    claims: List[ClaimSchema]
    report: CoachingReportResponse
