"""
Tests for 100-Point Communication Quality Evaluation Framework.
"""
import pytest
from services.quality_scorer import QualityScorer

def test_perfect_score_scenario():
    segments = [
        {"speaker_role": "customer", "text": "Does it have fast charging?"},
        {"speaker_role": "provider", "text": "Yes, it supports USB-C fast charging.", "is_off_topic": False, "topic_category": "direct_answer"}
    ]
    claims = [
        {"verification_status": "verified"}
    ]
    eval_result = QualityScorer.evaluate(
        segments=segments,
        claims=claims,
        customer_questions=["Does it have fast charging?"],
        answered_questions=["Does it have fast charging?"]
    )
    assert eval_result["overall_score"] == 100.0
    assert eval_result["breakdown"]["factual_accuracy"]["score"] == 30.0
    assert eval_result["breakdown"]["product_relevance"]["score"] == 25.0

def test_deductions_for_contradictions_and_off_topic():
    segments = [
        {"speaker_role": "customer", "text": "Is it waterproof?"},
        {
            "speaker_role": "provider",
            "text": "Yes 100% waterproof, and last month I went to Goa with my friend.",
            "is_off_topic": True,
            "topic_category": "off_topic_personal_discussion"
        }
    ]
    claims = [
        {"verification_status": "contradicted"}
    ]
    eval_result = QualityScorer.evaluate(
        segments=segments,
        claims=claims,
        customer_questions=["Is it waterproof?"],
        answered_questions=["Is it waterproof?"]
    )
    # Contradicted: -10 pts from Accuracy (30 -> 20)
    # Off-topic: -6 pts from Relevance (25 -> 19)
    assert eval_result["breakdown"]["factual_accuracy"]["score"] == 20.0
    assert eval_result["breakdown"]["product_relevance"]["score"] == 19.0
    assert len(eval_result["deductions"]) >= 2
