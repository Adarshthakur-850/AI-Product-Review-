"""
Speech-to-Text and Transcript Ingestion Service.
Supports audio transcription (Whisper adapter) and direct transcript parsing (JSON, CSV, Plain Text).
"""
import re
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pathlib import Path
from services.language_detector import LanguageDetector

class BaseSTTService(ABC):
    @abstractmethod
    def transcribe(self, file_path: Path) -> List[Dict[str, Any]]:
        """Transcribes audio file into timestamped segments with speaker tags."""
        pass

class MockWhisperSTTService(BaseSTTService):
    """
    Simulated Whisper STT adapter for testing and offline environments.
    Handles English, Hindi, and Hinglish with realistic timestamps.
    """
    def transcribe(self, file_path: Path) -> List[Dict[str, Any]]:
        # Returns structured sample segments if given an audio file
        return [
            {
                "speaker_role": "customer",
                "start_time": 0.0,
                "end_time": 3.5,
                "text": "Hello, is headphone ki battery kitni der chalti hai?",
                "confidence": 0.98
            },
            {
                "speaker_role": "provider",
                "start_time": 4.0,
                "end_time": 12.0,
                "text": "Sir, iska battery backup around 30 hours hai, aur waise mere friend ne bhi ye liya tha jab hum trip par gaye the.",
                "confidence": 0.95
            }
        ]

class TranscriptIngestionService:
    """
    Parses conversational transcripts from various formats:
    - Structured JSON list of turns
    - Formatted text (e.g. 'Customer [00:01]: ...', 'Provider: ...')
    """
    
    @staticmethod
    def parse_text_transcript(raw_text: str) -> List[Dict[str, Any]]:
        """
        Parses multi-line transcripts in formats:
        Customer: ...
        Provider: ...
        Agent: ...
        Buyer: ...
        """
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        segments = []
        current_time = 0.0
        
        for line in lines:
            role = "customer"
            text_body = line
            
            # Match speaker patterns
            speaker_match = re.match(r"^(Customer|User|Buyer|A)\s*(\[\d+:\d+\])?\s*:\s*(.*)$", line, re.IGNORECASE)
            if speaker_match:
                role = "customer"
                text_body = speaker_match.group(3).strip()
            else:
                provider_match = re.match(r"^(Provider|Agent|Salesperson|Representative|B)\s*(\[\d+:\d+\])?\s*:\s*(.*)$", line, re.IGNORECASE)
                if provider_match:
                    role = "provider"
                    text_body = provider_match.group(3).strip()
            
            lang_info = LanguageDetector.detect(text_body)
            duration = max(2.5, len(text_body.split()) * 0.4)
            
            segments.append({
                "speaker_role": role,
                "start_time": round(current_time, 2),
                "end_time": round(current_time + duration, 2),
                "text": text_body,
                "detected_language": lang_info["language"],
                "language_label": lang_info["label"],
                "confidence": lang_info["confidence"]
            })
            current_time += duration + 0.5
            
        return segments

    @staticmethod
    def parse_json_transcript(json_content: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Processes pre-structured JSON segments and enriches with language detection.
        """
        enriched = []
        for seg in json_content:
            text = seg.get("text", "")
            lang_info = LanguageDetector.detect(text)
            enriched.append({
                "speaker_role": seg.get("speaker_role", "customer").lower(),
                "start_time": float(seg.get("start_time", 0.0)),
                "end_time": float(seg.get("end_time", 0.0)),
                "text": text,
                "detected_language": lang_info["language"],
                "language_label": lang_info["label"],
                "confidence": float(seg.get("confidence", lang_info["confidence"]))
            })
        return enriched
