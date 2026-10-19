"""
100-Point Communication Quality and Compliance Evaluation Engine.
Evaluates:
- Factual Accuracy (30 pts)
- Product Relevance (25 pts)
- Answer Quality (20 pts)
- Conciseness (15 pts)
- Communication Clarity (10 pts)
"""
from typing import Dict, List, Any
from core.config import settings

class QualityScorer:
    """
    Computes a transparent 100-point communication score with detailed deduction audit trails.
    """
    
    @staticmethod
    def evaluate(
        segments: List[Dict[str, Any]],
        claims: List[Dict[str, Any]],
        customer_questions: List[str],
        answered_questions: List[str]
    ) -> Dict[str, Any]:
        """
        Executes rubric scoring across all 5 dimensions.
        """
        deductions = []
        
        # 1. FACTUAL ACCURACY (Max: 30 pts)
        accuracy_score = settings.SCORE_FACTUAL_ACCURACY
        contradicted_count = sum(1 for c in claims if c.get("verification_status") == "contradicted")
        unsupported_count = sum(1 for c in claims if c.get("verification_status") == "unsupported")
        
        if contradicted_count > 0:
            deduct_val = min(accuracy_score, contradicted_count * settings.DEDUCTION_CONTRADICTED_CLAIM)
            accuracy_score -= deduct_val
            deductions.append({
                "category": "Factual Accuracy",
                "deduction": deduct_val,
                "reason": f"{contradicted_count} claim(s) directly contradicted approved product documentation."
            })
            
        if unsupported_count > 0:
            deduct_val = min(accuracy_score, unsupported_count * settings.DEDUCTION_UNSUPPORTED_ASSERTION)
            accuracy_score -= deduct_val
            deductions.append({
                "category": "Factual Accuracy",
                "deduction": deduct_val,
                "reason": f"{unsupported_count} unverified claim(s) made without approved documentation."
            })
            
        accuracy_score = max(0.0, round(accuracy_score, 1))

        # 2. PRODUCT RELEVANCE (Max: 25 pts)
        relevance_score = settings.SCORE_PRODUCT_RELEVANCE
        off_topic_segments = [s for s in segments if s.get("speaker_role") == "provider" and s.get("is_off_topic")]
        
        if off_topic_segments:
            deduct_val = min(relevance_score, len(off_topic_segments) * settings.DEDUCTION_OFF_TOPIC_STORY)
            relevance_score -= deduct_val
            deductions.append({
                "category": "Product Relevance",
                "deduction": deduct_val,
                "reason": f"{len(off_topic_segments)} off-topic personal discussion / unrelated segment(s) identified."
            })
        relevance_score = max(0.0, round(relevance_score, 1))

        # 3. ANSWER QUALITY (Max: 20 pts)
        answer_score = settings.SCORE_ANSWER_QUALITY
        missed_questions = [q for q in customer_questions if q not in answered_questions]
        
        if missed_questions:
            deduct_val = min(answer_score, len(missed_questions) * settings.DEDUCTION_MISSED_QUESTION)
            answer_score -= deduct_val
            deductions.append({
                "category": "Answer Quality",
                "deduction": deduct_val,
                "reason": f"{len(missed_questions)} explicit customer question(s) left unresolved or unanswered."
            })
        answer_score = max(0.0, round(answer_score, 1))

        # 4. CONCISENESS (Max: 15 pts)
        conciseness_score = settings.SCORE_CONCISENESS
        repetitive_segments = [s for s in segments if s.get("topic_category") == "repetition_unnecessary_elaboration"]
        
        if repetitive_segments:
            deduct_val = min(conciseness_score, len(repetitive_segments) * settings.DEDUCTION_CIRCULAR_REPETITION)
            conciseness_score -= deduct_val
            deductions.append({
                "category": "Conciseness",
                "deduction": deduct_val,
                "reason": f"{len(repetitive_segments)} repetitive or unnecessarily prolonged statement(s)."
            })
        conciseness_score = max(0.0, round(conciseness_score, 1))

        # 5. COMMUNICATION CLARITY (Max: 10 pts)
        clarity_score = settings.SCORE_COMMUNICATION_CLARITY
        provider_segments = [s for s in segments if s.get("speaker_role") == "provider"]
        
        # Check for extreme wordiness or filler density
        long_turns = sum(1 for s in provider_segments if len(s.get("text", "").split()) > 60)
        if long_turns > 0:
            deduct_val = min(clarity_score, long_turns * 3.0)
            clarity_score -= deduct_val
            deductions.append({
                "category": "Communication Clarity",
                "deduction": deduct_val,
                "reason": f"{long_turns} turn(s) were overly lengthy without customer-paced pausing."
            })
        clarity_score = max(0.0, round(clarity_score, 1))

        overall_score = round(accuracy_score + relevance_score + answer_score + conciseness_score + clarity_score, 1)

        # Performance Tier
        if overall_score >= 85:
            tier = "Exemplary Compliance & Communication"
        elif overall_score >= 70:
            tier = "Proficient (Minor Polish Needed)"
        elif overall_score >= 50:
            tier = "Coaching Recommended"
        else:
            tier = "Priority Training Required"

        return {
            "overall_score": overall_score,
            "tier": tier,
            "breakdown": {
                "factual_accuracy": {
                    "score": accuracy_score,
                    "max": settings.SCORE_FACTUAL_ACCURACY,
                    "percentage": round((accuracy_score / settings.SCORE_FACTUAL_ACCURACY) * 100, 1)
                },
                "product_relevance": {
                    "score": relevance_score,
                    "max": settings.SCORE_PRODUCT_RELEVANCE,
                    "percentage": round((relevance_score / settings.SCORE_PRODUCT_RELEVANCE) * 100, 1)
                },
                "answer_quality": {
                    "score": answer_score,
                    "max": settings.SCORE_ANSWER_QUALITY,
                    "percentage": round((answer_score / settings.SCORE_ANSWER_QUALITY) * 100, 1)
                },
                "conciseness": {
                    "score": conciseness_score,
                    "max": settings.SCORE_CONCISENESS,
                    "percentage": round((conciseness_score / settings.SCORE_CONCISENESS) * 100, 1)
                },
                "communication_clarity": {
                    "score": clarity_score,
                    "max": settings.SCORE_COMMUNICATION_CLARITY,
                    "percentage": round((clarity_score / settings.SCORE_COMMUNICATION_CLARITY) * 100, 1)
                }
            },
            "deductions": deductions,
            "metrics": {
                "total_claims": len(claims),
                "verified_claims": sum(1 for c in claims if c.get("verification_status") == "verified"),
                "contradicted_claims": contradicted_count,
                "unsupported_claims": unsupported_count,
                "off_topic_segments": len(off_topic_segments),
                "missed_questions": len(missed_questions)
            }
        }
