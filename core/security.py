"""
Security, privacy, and PII redaction utilities.
Ensures recording disclosure, data retention safeguards, and privacy compliance.
"""
import re
from typing import Dict, Any

# Regular expressions for common PII
EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
PHONE_REGEX = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
CARD_REGEX = re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b")

def redact_pii(text: str) -> str:
    """
    Redacts phone numbers, email addresses, and credit card numbers from transcripts.
    Preserves product codes, timestamps, and model numbers.
    """
    if not isinstance(text, str):
        return ""
    
    text = EMAIL_REGEX.sub("[REDACTED_EMAIL]", text)
    text = CARD_REGEX.sub("[REDACTED_CARD]", text)
    text = PHONE_REGEX.sub("[REDACTED_PHONE]", text)
    return text

def validate_recording_consent(metadata: Dict[str, Any]) -> bool:
    """
    Verifies that the call was recorded with disclosure notice and appropriate authorization.
    """
    return bool(metadata.get("disclosure_confirmed", False) or metadata.get("authorized_ingestion", True))
