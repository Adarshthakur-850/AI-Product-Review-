"""
FastAPI Routes for Service Provider Performance Analytics & Compliance Tracking.
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter(prefix="/providers", tags=["Provider Performance Analytics"])

# Representative provider registry
PROVIDERS_DB = {
    "rohan-sharma": {
        "id": "rohan-sharma",
        "name": "Rohan Sharma",
        "department": "Consumer Electronics Sales",
        "total_calls": 14,
        "average_score": 76.5,
        "language_distribution": {"Hinglish": 9, "English": 3, "Hindi": 2},
        "score_trends": [
            {"call_index": 1, "score": 68.0},
            {"call_index": 2, "score": 72.5},
            {"call_index": 3, "score": 74.0},
            {"call_index": 4, "score": 81.5}
        ],
        "top_improvement_areas": [
            "Avoid sharing personal vacation/friend anecdotes during technical queries",
            "Double-check IPX4 splash resistance vs waterproof claims for audio gear",
            "Keep answers concise and allow customer follow-ups"
        ]
    },
    "priya-verma": {
        "id": "priya-verma",
        "name": "Priya Verma",
        "department": "Smartphone Customer Support",
        "total_calls": 22,
        "average_score": 92.0,
        "language_distribution": {"Hindi": 12, "Hinglish": 8, "English": 2},
        "score_trends": [
            {"call_index": 1, "score": 88.0},
            {"call_index": 2, "score": 90.5},
            {"call_index": 3, "score": 94.0},
            {"call_index": 4, "score": 95.5}
        ],
        "top_improvement_areas": [
            "Maintain current high standard of factual compliance",
            "Offer trade-in bonus information proactively"
        ]
    }
}

@router.get("")
async def list_providers():
    """Lists registered service providers."""
    return list(PROVIDERS_DB.values())

@router.get("/{provider_id}/performance")
async def get_provider_performance(provider_id: str):
    """Retrieves longitudinal performance trends, average scores, and recurring issues."""
    slug = provider_id.lower().replace(" ", "-")
    if slug not in PROVIDERS_DB:
        raise HTTPException(status_code=404, detail=f"Provider '{provider_id}' not found.")
    return PROVIDERS_DB[slug]
