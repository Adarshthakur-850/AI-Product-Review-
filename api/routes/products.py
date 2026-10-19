"""
FastAPI Routes for Product Knowledge Base and Approved Documentation.
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import json
from pathlib import Path

from api.schemas.product_schema import ProductCreate, ProductResponse, ProductDocumentCreate
from services.knowledge_base import ProductKnowledgeBase
from core.config import settings

router = APIRouter(prefix="/products", tags=["Product Knowledge Base"])
kb = ProductKnowledgeBase()

@router.get("", response_model=List[ProductResponse])
async def list_products():
    """Lists all approved products in the catalog."""
    kb.reload_catalogs()
    return kb.list_products()

@router.get("/{product_id}")
async def get_product(product_id: str):
    """Retrieves full specification and commercial terms for a product."""
    prod = kb.get_product(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found in approved catalog.")
    return prod

@router.post("", response_model=ProductResponse)
async def create_product(product: ProductCreate):
    """Registers a new approved product into the knowledge base."""
    target_file = settings.CATALOG_DIR / f"{product.id}.json"
    
    prod_data = product.model_dump()
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(prod_data, f, indent=2, ensure_ascii=False)
        
    kb.reload_catalogs()
    return ProductResponse(
        id=product.id,
        name=product.name,
        category=product.category,
        brand=product.brand,
        version="1.0",
        is_active=True
    )

@router.post("/{product_id}/documents")
async def add_product_document(product_id: str, doc: ProductDocumentCreate):
    """Appends an approved document/specification to an existing product."""
    prod = kb.get_product(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found.")
        
    if "specifications" not in prod:
        prod["specifications"] = {}
    prod["specifications"][doc.title.lower().replace(" ", "_")] = doc.content
    
    target_file = settings.CATALOG_DIR / f"{product_id}.json"
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(prod, f, indent=2, ensure_ascii=False)
        
    kb.reload_catalogs()
    return {"status": "success", "message": f"Document '{doc.title}' appended to product '{product_id}'."}
