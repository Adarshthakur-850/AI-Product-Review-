"""
Pydantic schemas for Product Catalog and Documentation management.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class ProductDocumentCreate(BaseModel):
    title: str
    doc_type: str = "specification"  # spec, pricing, warranty, faq, policy
    content: str
    version: str = "1.0"

class ProductCreate(BaseModel):
    id: str = Field(..., description="Unique product slug/id (e.g. quantum-sound-pro)")
    name: str
    category: str
    brand: str = "QuantumTech"
    specifications: Dict[str, Any] = {}
    commercial_terms: Dict[str, Any] = {}
    policies: Dict[str, Any] = {}
    frequently_asked_questions: List[Dict[str, str]] = []

class ProductResponse(BaseModel):
    id: str
    name: str
    category: str
    brand: str
    version: Optional[str] = "1.0"
    is_active: bool = True
