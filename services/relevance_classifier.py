"""
Conversational Relevance and Topic Classification Service.
Classifies provider conversational turns into 10 standard compliance categories.
Considers conversational context, customer questions, and social greetings.
"""
import re
from typing import Dict, Any, List, Optional

class RelevanceCategory:
    DIRECT_ANSWER = "direct_answer"
    RELEVANT_FEATURE = "relevant_product_feature"
    PRICE_AVAILABILITY = "relevant_price_availability"
    NECESSARY_CLARIFICATION = "necessary_clarification"
    RELEVANT_RECOMMENDATION = "relevant_recommendation"
    POLITE_SOCIAL = "polite_social_interaction"
    REPETITION_ELABORATION = "repetition_unnecessary_elaboration"
    OFF_TOPIC_PERSONAL = "off_topic_personal_discussion"
    UNSUPPORTED_CLAIM = "unsupported_product_claim"
    MISLEADING_CONTRADICTORY = "potentially_misleading_statement"

CATEGORY_LABELS = {
    RelevanceCategory.DIRECT_ANSWER: "Direct Answer to Customer Question",
    RelevanceCategory.RELEVANT_FEATURE: "Relevant Product Feature",
    RelevanceCategory.PRICE_AVAILABILITY: "Price or Availability Information",
    RelevanceCategory.NECESSARY_CLARIFICATION: "Necessary Clarification",
    RelevanceCategory.RELEVANT_RECOMMENDATION: "Relevant Recommendation / Comparison",
    RelevanceCategory.POLITE_SOCIAL: "Polite Social Interaction / Greeting",
    RelevanceCategory.REPETITION_ELABORATION: "Repetition or Unnecessary Elaboration",
    RelevanceCategory.OFF_TOPIC_PERSONAL: "Off-Topic Personal Discussion",
    RelevanceCategory.UNSUPPORTED_CLAIM: "Unsupported Product Claim",
    RelevanceCategory.MISLEADING_CONTRADICTORY: "Potentially Misleading / Contradictory"
}

# Regex patterns for social greetings (English, Hindi, Hinglish)
GREETING_PATTERNS = re.compile(
    r"\b(hello|hi|good morning|good afternoon|good evening|welcome|namaste|pranam|shukriya|thank you|thanks|have a nice day|alvida|bye)\b",
    re.IGNORECASE
)

# Regex patterns for personal anecdotes / off-topic stories
PERSONAL_STORY_PATTERNS = re.compile(
    r"\b((?:mere|mera|meri|my)\s+(?:friend|dost|cousin|bhai|sister|family)|last trip|last vacation|trip par|hum ghumne|ghumne gaye|humne bohot enjoy|personal experience|apni baat bataun|humare gaon|family function)\b",
    re.IGNORECASE
)

# Clarification request patterns
CLARIFICATION_PATTERNS = re.compile(
    r"\b(can you please specify|which color|what is your budget|aapka budget kya hai|konsa color chahiye|aapko kiske liye chahiye|could you clarify)\b",
    re.IGNORECASE
)

# Price / availability inquiry patterns
PRICE_PATTERNS = re.compile(
    r"\b(price|cost|inr|rs|rupees|discount|offer|emi|in stock|available|delivery time|kitne ka|dam|keemat|chhoot)\b",
    re.IGNORECASE
)

class RelevanceClassifier:
    """
    Evaluates whether each conversational turn by the provider is relevant,
    polite, repetitive, off-topic, or misleading.
    """
    
    @staticmethod
    def classify_turn(
        current_text: str,
        last_customer_question: Optional[str] = None,
        is_contradicted: bool = False,
        is_unsupported: bool = False,
        repeated_count: int = 0
    ) -> Dict[str, Any]:
        """
        Classifies provider statement into one of the 10 compliance categories.
        """
        text = current_text.strip()
        lower_text = text.lower()
        
        # 1. Contradicted or Misleading
        if is_contradicted:
            return {
                "category": RelevanceCategory.MISLEADING_CONTRADICTORY,
                "label": CATEGORY_LABELS[RelevanceCategory.MISLEADING_CONTRADICTORY],
                "is_off_topic": False,
                "confidence": 0.95,
                "explanation": "Statement directly contradicts verified product documentation."
            }
            
        # 2. Unsupported Claim
        if is_unsupported:
            return {
                "category": RelevanceCategory.UNSUPPORTED_CLAIM,
                "label": CATEGORY_LABELS[RelevanceCategory.UNSUPPORTED_CLAIM],
                "is_off_topic": False,
                "confidence": 0.90,
                "explanation": "Provider made an affirmative claim without evidence in approved documentation."
            }
            
        # 3. Off-Topic Personal Discussion (e.g. personal trips, friends, unrelated anecdotes)
        if PERSONAL_STORY_PATTERNS.search(lower_text):
            return {
                "category": RelevanceCategory.OFF_TOPIC_PERSONAL,
                "label": CATEGORY_LABELS[RelevanceCategory.OFF_TOPIC_PERSONAL],
                "is_off_topic": True,
                "confidence": 0.92,
                "explanation": "Contains personal anecdote or story unrelated to solving the customer's query."
            }
            
        # 4. Repetition or Unnecessary Elaboration
        if repeated_count >= 2:
            return {
                "category": RelevanceCategory.REPETITION_ELABORATION,
                "label": CATEGORY_LABELS[RelevanceCategory.REPETITION_ELABORATION],
                "is_off_topic": False,
                "confidence": 0.88,
                "explanation": "Provider repeated this information multiple times unnecessarily."
            }

        # 5. Polite Social Interaction (greetings, courtesies)
        if GREETING_PATTERNS.search(lower_text) and len(text.split()) <= 15:
            return {
                "category": RelevanceCategory.POLITE_SOCIAL,
                "label": CATEGORY_LABELS[RelevanceCategory.POLITE_SOCIAL],
                "is_off_topic": False,
                "confidence": 0.95,
                "explanation": "Courteous greeting or professional closing; legitimate interaction."
            }

        # 6. Necessary Clarification
        if CLARIFICATION_PATTERNS.search(lower_text) or "?" in text:
            return {
                "category": RelevanceCategory.NECESSARY_CLARIFICATION,
                "label": CATEGORY_LABELS[RelevanceCategory.NECESSARY_CLARIFICATION],
                "is_off_topic": False,
                "confidence": 0.90,
                "explanation": "Provider requested clarifying requirements to better assist the customer."
            }

        # 7. Price and Commercial Details
        if PRICE_PATTERNS.search(lower_text):
            return {
                "category": RelevanceCategory.PRICE_AVAILABILITY,
                "label": CATEGORY_LABELS[RelevanceCategory.PRICE_AVAILABILITY],
                "is_off_topic": False,
                "confidence": 0.92,
                "explanation": "Addresses commercial pricing, discounts, warranty, or availability."
            }

        # 8. Direct Answer to Customer's Question
        if last_customer_question:
            # Check overlap between customer's question and provider's response
            q_words = set(re.findall(r"\w+", last_customer_question.lower()))
            ans_words = set(re.findall(r"\w+", lower_text))
            if len(q_words & ans_words) >= 2 or any(k in lower_text for k in ["yes", "no", "haan", "nahi", "available", "hours", "mah"]):
                return {
                    "category": RelevanceCategory.DIRECT_ANSWER,
                    "label": CATEGORY_LABELS[RelevanceCategory.DIRECT_ANSWER],
                    "is_off_topic": False,
                    "confidence": 0.88,
                    "explanation": "Directly resolves the specific question posed by the customer."
                }

        # 9. General Relevant Feature / Recommendation
        return {
            "category": RelevanceCategory.RELEVANT_FEATURE,
            "label": CATEGORY_LABELS[RelevanceCategory.RELEVANT_FEATURE],
            "is_off_topic": False,
            "confidence": 0.85,
            "explanation": "Explains product specification, capability, or legitimate comparison."
        }
