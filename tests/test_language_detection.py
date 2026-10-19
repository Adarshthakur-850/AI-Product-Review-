"""
Tests for Multilingual Language Identification Service.
Validates English, Hindi (Devanagari), and Hinglish (Code-switched).
"""
import pytest
from services.language_detector import LanguageDetector

def test_detect_english():
    text = "Does the Quantum Sound Pro support dual device pairing with my laptop?"
    result = LanguageDetector.detect(text)
    assert result["language"] == "en"
    assert result["is_code_switched"] is False

def test_detect_devanagari_hindi():
    text = "नमस्ते, क्या एपेक्स 15 प्रो में वायरलेस चार्जिंग का सपोर्ट मिलता है?"
    result = LanguageDetector.detect(text)
    assert result["language"] == "hi"
    assert result["script"] == "devanagari"

def test_detect_hinglish_code_switched():
    text = "Sir, iska battery backup around 30 hours hai, aur isme fast charging bhi milti hai."
    result = LanguageDetector.detect(text)
    assert result["language"] == "hi-Latn"
    assert result["is_code_switched"] is True

def test_detect_hinglish_with_technical_terms():
    text = "Camera me OIS support hai ya sirf EIS milta hai?"
    result = LanguageDetector.detect(text)
    assert result["language"] == "hi-Latn"

def test_detect_empty_or_whitespace():
    result = LanguageDetector.detect("")
    assert result["language"] == "en"
