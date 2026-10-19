"""
End-to-end regression tests covering the 3 multilingual benchmark cases.
Validates English, Hindi, and Hinglish audit workflows.
"""
import pytest
import json
from services.auditor_pipeline import ProductGuardAuditorPipeline

@pytest.fixture
def pipeline():
    return ProductGuardAuditorPipeline()

def test_benchmark_case_1_hinglish(pipeline):
    with open("data/sample_conversations/call_01_hinglish_earbuds.json", "r", encoding="utf-8") as f:
        case = json.load(f)
    result = pipeline.audit_conversation(
        call_id=case["call_id"],
        product_id=case["product_id"],
        provider_name=case["provider_name"],
        structured_segments=case["segments"],
        target_report_language="Hinglish"
    )
    eval_data = result["evaluation"]
    assert eval_data["metrics"]["contradicted_claims"] == 1  # Swimming waterproof claim contradicted
    assert eval_data["metrics"]["off_topic_segments"] == 1   # Goa vacation story flagged
    assert eval_data["overall_score"] < 85.0
    assert len(result["report"]["suggested_replacements"]) >= 1

def test_benchmark_case_2_hindi(pipeline):
    with open("data/sample_conversations/call_02_hindi_phone.json", "r", encoding="utf-8") as f:
        case = json.load(f)
    result = pipeline.audit_conversation(
        call_id=case["call_id"],
        product_id=case["product_id"],
        provider_name=case["provider_name"],
        structured_segments=case["segments"],
        target_report_language="Hindi"
    )
    eval_data = result["evaluation"]
    assert eval_data["overall_score"] >= 95.0
    assert eval_data["metrics"]["verified_claims"] >= 2
    assert eval_data["metrics"]["contradicted_claims"] == 0

def test_benchmark_case_3_english(pipeline):
    with open("data/sample_conversations/call_03_english_laptop.json", "r", encoding="utf-8") as f:
        case = json.load(f)
    result = pipeline.audit_conversation(
        call_id=case["call_id"],
        product_id=case["product_id"],
        provider_name=case["provider_name"],
        structured_segments=case["segments"],
        target_report_language="English"
    )
    eval_data = result["evaluation"]
    assert eval_data["overall_score"] == 100.0
    assert eval_data["metrics"]["missed_questions"] == 0
