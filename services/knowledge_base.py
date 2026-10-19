"""
Product Knowledge Base (RAG) Service.
Indexes approved product specifications, commercial terms, policies, and FAQs.
Provides grounded factual retrieval for claim verification.
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from core.config import settings

class ProductKnowledgeBase:
    """
    Retrieves verified product facts from approved catalogs.
    Strictly grounds answers; never hallucinates missing specifications.
    """
    def __init__(self, catalog_dir: Path = None):
        self.catalog_dir = catalog_dir or settings.CATALOG_DIR
        self.catalogs: Dict[str, Dict[str, Any]] = {}
        self.indexed_facts: Dict[str, List[Dict[str, Any]]] = {}
        self.reload_catalogs()

    def reload_catalogs(self):
        """Scans catalog directory and builds in-memory factual indexes."""
        self.catalogs.clear()
        self.indexed_facts.clear()
        
        if not self.catalog_dir.exists():
            return

        for filepath in self.catalog_dir.glob("*.json"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    prod_id = data.get("id")
                    if prod_id:
                        self.catalogs[prod_id] = data
                        self._index_product(prod_id, data)
            except Exception as e:
                print(f"Error loading catalog file {filepath}: {e}")

    def _index_product(self, product_id: str, data: Dict[str, Any]):
        """Splits product knowledge into searchable atomic facts."""
        facts = []
        prod_name = data.get("name", product_id)
        
        # 1. Index specifications
        for key, val in data.get("specifications", {}).items():
            facts.append({
                "product_id": product_id,
                "category": "specification",
                "attribute": key,
                "fact_text": f"{key.replace('_', ' ').title()}: {val}",
                "source": f"{prod_name} Spec Sheet v{data.get('version', '1.0')}",
                "keywords": set(re.findall(r"\w+", f"{key} {val}".lower()))
            })
            
        # 2. Index commercial terms
        for key, val in data.get("commercial_terms", {}).items():
            facts.append({
                "product_id": product_id,
                "category": "commercial_terms",
                "attribute": key,
                "fact_text": f"{key.replace('_', ' ').title()}: {val}",
                "source": f"{prod_name} Pricing Policy v{data.get('version', '1.0')}",
                "keywords": set(re.findall(r"\w+", f"{key} {val}".lower()))
            })
            
        # 3. Index policies & warranties
        for key, val in data.get("policies", {}).items():
            facts.append({
                "product_id": product_id,
                "category": "policy",
                "attribute": key,
                "fact_text": f"{key.replace('_', ' ').title()}: {val}",
                "source": f"{prod_name} Terms & Warranty v{data.get('version', '1.0')}",
                "keywords": set(re.findall(r"\w+", f"{key} {val}".lower()))
            })
            
        # 4. Index FAQs
        for idx, faq in enumerate(data.get("frequently_asked_questions", [])):
            q = faq.get("question", "")
            a = faq.get("answer", "")
            facts.append({
                "product_id": product_id,
                "category": "faq",
                "attribute": f"faq_{idx+1}",
                "fact_text": f"Q: {q} | A: {a}",
                "source": f"{prod_name} Approved FAQs",
                "keywords": set(re.findall(r"\w+", f"{q} {a}".lower()))
            })

        self.indexed_facts[product_id] = facts

    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        return self.catalogs.get(product_id)

    def list_products(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": p["id"],
                "name": p["name"],
                "category": p["category"],
                "brand": p.get("brand", ""),
                "version": p.get("version", "1.0")
            }
            for p in self.catalogs.values()
        ]

    def search_facts(self, product_id: str, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Hybrid retrieval: Lexical keyword overlap score + attribute matching.
        """
        if product_id not in self.indexed_facts:
            return []
        
        query_words = set(re.findall(r"\w+", query.lower()))
        if not query_words:
            return []
        
        scored_facts = []
        for item in self.indexed_facts[product_id]:
            # Jaccard / word overlap similarity
            overlap = len(query_words & item["keywords"])
            if overlap > 0:
                score = overlap / len(query_words | item["keywords"])
                # Boost if query mentions attribute directly (e.g. 'battery', 'price', 'warranty')
                if item["attribute"].lower() in query.lower():
                    score += 0.5
                scored_facts.append((score, item))
        
        scored_facts.sort(key=lambda x: x[0], reverse=True)
        return [fact for _, fact in scored_facts[:top_k]]
