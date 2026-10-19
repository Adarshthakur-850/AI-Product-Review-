"""
Tests for Product Claim Extraction and Knowledge Base Verification.
Validates VERIFIED, CONTRADICTED, and UNSUPPORTED status handling.
"""
import pytest
from services.knowledge_base import ProductKnowledgeBase
from services.claim_verifier import ClaimVerifier

@pytest.fixture
def claim_verifier():
    kb = ProductKnowledgeBase()
    return ClaimVerifier(kb)

def test_verify_accurate_battery_claim(claim_verifier):
    statement = "Sir, iska battery backup around 30 hours hai with ANC off."
    claims = claim_verifier.extract_and_verify(
        provider_statement=statement,
        product_id="quantum-sound-pro"
    )
    assert len(claims) >= 1
    battery_claim = [c for c in claims if c["category"] == "battery"][0]
    assert battery_claim["verification_status"] == "verified"

def test_contradict_waterproof_claim(claim_verifier):
    statement = "Ye 100% waterproof hai aap swimming pool me aaram se use kar sakte ho."
    claims = claim_verifier.extract_and_verify(
        provider_statement=statement,
        product_id="quantum-sound-pro"
    )
    water_claim = [c for c in claims if c["category"] == "water_resistance"][0]
    assert water_claim["verification_status"] == "contradicted"
    assert "splash" in water_claim["explanation"].lower() or "swimming" in water_claim["explanation"].lower()

def test_contradict_wireless_charging_on_phone(claim_verifier):
    statement = "Haan sir isme wireless charging bhi support karta hai."
    claims = claim_verifier.extract_and_verify(
        provider_statement=statement,
        product_id="apex-phone-15"
    )
    charging_claim = [c for c in claims if c["category"] == "charging"][0]
    assert charging_claim["verification_status"] == "contradicted"

def test_verify_accurate_price(claim_verifier):
    statement = "Abhi launch offer me ye flat INR 5,999 me mil jayega."
    claims = claim_verifier.extract_and_verify(
        provider_statement=statement,
        product_id="quantum-sound-pro"
    )
    price_claim = [c for c in claims if c["category"] == "pricing"][0]
    assert price_claim["verification_status"] == "verified"
