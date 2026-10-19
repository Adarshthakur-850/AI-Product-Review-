"""
Integration tests for FastAPI REST Endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["system"] == "ProductGuard AI"
    assert data["status"] == "operational"

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_list_products():
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) >= 2
    ids = [p["id"] for p in products]
    assert "quantum-sound-pro" in ids
    assert "apex-phone-15" in ids

def test_audit_call_endpoint():
    payload = {
        "product_id": "quantum-sound-pro",
        "provider_name": "Rohan Sharma",
        "customer_name": "Amit Patel",
        "disclosure_confirmed": True,
        "target_report_language": "Hinglish",
        "raw_transcript": (
            "Customer: Is headphone ki battery kitni der chalti hai?\n"
            "Provider: Sir iska battery backup around 30 hours hai."
        )
    }
    response = client.post("/api/v1/calls", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert "report" in data
    assert data["report"]["overall_score"] > 80.0

def test_realtime_turn_endpoint():
    response = client.post("/api/v1/calls/realtime-turn", params={
        "product_id": "quantum-sound-pro",
        "turn_text": "Sir, iska battery backup around 30 hours hai with ANC off.",
        "speaker_role": "provider",
        "target_language": "Hinglish"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["alert_type"] == "SUCCESS"
    assert len(data["claims"]) >= 1

def test_provider_performance_endpoint():
    response = client.get("/api/v1/providers/rohan-sharma/performance")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Rohan Sharma"
    assert "average_score" in data
