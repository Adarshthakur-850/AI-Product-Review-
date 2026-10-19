"""
Language Identification Service.
Detects English ('en'), Devanagari Hindi ('hi'), and Hinglish/Romanized Hindi ('hi-Latn')
at the utterance or sentence level.
"""
import re
from typing import Dict, Any

# Devanagari Unicode Block: \u0900-\u097F
DEVANAGARI_REGEX = re.compile(r"[\u0900-\u097F]")

# Common Romanized Hindi / Hinglish grammatical markers & function words
HINGLISH_MARKERS = {
    "hai", "hain", "ho", "hu", "hoon", "tha", "the", "thi", "ka", "ki", "ke",
    "ko", "se", "me", "mein", "par", "pe", "aur", "ya", "lekin", "magar", "parantu",
    "iska", "iski", "iske", "uska", "uski", "uske", "kya", "kyun", "kyu", "kaise",
    "kab", "kaha", "kahan", "kitna", "kitni", "kitne", "nahi", "nhi", "na", "mat",
    "bhi", "hi", "to", "toh", "sir", "ji", "bhai", "aap", "tum", "hum", "main",
    "karo", "kare", "karna", "milti", "milta", "milenge", "chahiye", "hoga", "hogi",
    "honge", "sakta", "sakti", "sakte", "accha", "achha", "bohot", "bahut", "thik",
    "shukriya", "dhanyawad", "waise", "bol", "raha", "rahe", "rahi", "chalega", "dega"
}

# Common English function words
ENGLISH_MARKERS = {
    "the", "is", "are", "am", "was", "were", "this", "that", "these", "those",
    "and", "or", "but", "with", "for", "from", "at", "by", "in", "on", "to",
    "can", "will", "would", "should", "could", "have", "has", "had", "does", "do",
    "product", "feature", "battery", "price", "discount", "warranty", "screen"
}

class LanguageDetector:
    """
    Identifies language mode at the sentence or utterance level.
    Distinguishes English ('en'), Devanagari Hindi ('hi'), and Hinglish ('hi-Latn').
    """
    
    @staticmethod
    def detect(text: str) -> Dict[str, Any]:
        """
        Analyzes text and returns detected language code and label with confidence.
        """
        if not text or not text.strip():
            return {
                "language": "en",
                "label": "English",
                "confidence": 1.0,
                "is_code_switched": False,
                "script": "latin"
            }
        
        raw_text = text.strip()
        total_chars = len(raw_text)
        
        # Check Devanagari script presence
        devanagari_chars = len(DEVANAGARI_REGEX.findall(raw_text))
        devanagari_ratio = devanagari_chars / total_chars if total_chars > 0 else 0.0
        
        if devanagari_ratio > 0.25:
            # Significant Devanagari script detected
            has_latin = bool(re.search(r"[A-Za-z]", raw_text))
            if has_latin and devanagari_ratio < 0.80:
                return {
                    "language": "hi-Latn",
                    "label": "Hinglish (Devanagari + English Mixed)",
                    "confidence": round(0.85 + (devanagari_ratio * 0.1), 2),
                    "is_code_switched": True,
                    "script": "mixed"
                }
            return {
                "language": "hi",
                "label": "Hindi (Devanagari)",
                "confidence": round(min(0.99, 0.7 + devanagari_ratio * 0.3), 2),
                "is_code_switched": False,
                "script": "devanagari"
            }
        
        # Text is in Latin alphabet: Check for Hinglish vs pure English
        tokens = re.findall(r"\b[A-Za-z'-]+\b", raw_text.lower())
        if not tokens:
            return {
                "language": "en",
                "label": "English",
                "confidence": 0.8,
                "is_code_switched": False,
                "script": "latin"
            }
        
        token_count = len(tokens)
        hinglish_hits = sum(1 for t in tokens if t in HINGLISH_MARKERS)
        english_hits = sum(1 for t in tokens if t in ENGLISH_MARKERS)
        
        hinglish_ratio = hinglish_hits / token_count
        
        # If there are distinctive Hinglish tokens
        if hinglish_hits >= 1 and (hinglish_ratio >= 0.15 or hinglish_hits >= 2):
            return {
                "language": "hi-Latn",
                "label": "Hinglish",
                "confidence": round(min(0.98, 0.65 + hinglish_ratio * 0.35), 2),
                "is_code_switched": True,
                "script": "latin"
            }
        
        return {
            "language": "en",
            "label": "English",
            "confidence": round(min(0.99, 0.70 + (english_hits / max(1, token_count)) * 0.3), 2),
            "is_code_switched": False,
            "script": "latin"
        }
