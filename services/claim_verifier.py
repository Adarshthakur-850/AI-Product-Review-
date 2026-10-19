"""
Product Claim Extraction and Verification Engine.
Extracts atomic assertions from provider statements and verifies them
against the approved Product Knowledge Base.
Categorizes claims as VERIFIED, CONTRADICTED, UNSUPPORTED, or AMBIGUOUS.
"""
import re
from typing import List, Dict, Any
from services.knowledge_base import ProductKnowledgeBase

class ClaimVerifier:
    """
    Extracts and audits factual claims made during conversations.
    """
    def __init__(self, kb: ProductKnowledgeBase):
        self.kb = kb

    def extract_and_verify(
        self,
        provider_statement: str,
        product_id: str,
        timestamp: float = 0.0,
        segment_id: str = None
    ) -> List[Dict[str, Any]]:
        """
        Parses provider text, isolates factual claims, and evaluates against catalog truth.
        """
        claims = []
        product = self.kb.get_product(product_id)
        if not product:
            return []

        lower_text = provider_statement.lower()
        specs = product.get("specifications", {})
        terms = product.get("commercial_terms", {})
        policies = product.get("policies", {})

        # --- 1. Battery Claims Extraction ---
        battery_match = re.search(r"(\b\d+\s*(?:hours|hrs|ghante|mah)\b)", lower_text)
        if "battery" in lower_text or battery_match:
            claimed_val = battery_match.group(1) if battery_match else "battery claims"
            approved_battery = specs.get("battery_life") or specs.get("battery")
            
            if approved_battery:
                # Check consistency
                # e.g., if claimed 50 hours when spec is 30 hours
                numbers_in_claim = re.findall(r"\b\d+\b", claimed_val)
                numbers_in_spec = re.findall(r"\b\d+\b", approved_battery)
                
                is_contradicted = False
                if numbers_in_claim and numbers_in_spec:
                    if int(numbers_in_claim[0]) > int(numbers_in_spec[0]):
                        is_contradicted = True
                
                if is_contradicted:
                    claims.append({
                        "original_statement": provider_statement,
                        "timestamp": timestamp,
                        "segment_id": segment_id,
                        "category": "battery",
                        "claim_text": f"Battery runtime of {claimed_val}",
                        "verification_status": "contradicted",
                        "supporting_source": f"{product['name']} Spec Sheet",
                        "supporting_excerpt": approved_battery,
                        "explanation": f"Claimed {claimed_val}, but verified specification states: {approved_battery}.",
                        "corrected_text": f"Battery life is {approved_battery}.",
                        "confidence": 0.95
                    })
                else:
                    claims.append({
                        "original_statement": provider_statement,
                        "timestamp": timestamp,
                        "segment_id": segment_id,
                        "category": "battery",
                        "claim_text": f"Battery runtime of {claimed_val}",
                        "verification_status": "verified",
                        "supporting_source": f"{product['name']} Spec Sheet",
                        "supporting_excerpt": approved_battery,
                        "explanation": "Claim aligns with official battery specifications.",
                        "corrected_text": None,
                        "confidence": 0.96
                    })
            else:
                claims.append({
                    "original_statement": provider_statement,
                    "timestamp": timestamp,
                    "segment_id": segment_id,
                    "category": "battery",
                    "claim_text": f"Battery runtime of {claimed_val}",
                    "verification_status": "unsupported",
                    "supporting_source": "Catalog Check",
                    "supporting_excerpt": "No battery specification recorded in catalog.",
                    "explanation": "Unverified — insufficient product information in approved catalog.",
                    "corrected_text": "Verify official battery runtime before quoting to customers.",
                    "confidence": 0.85
                })

        # --- 2. Waterproof / Water Resistance Claims ---
        if any(w in lower_text for w in ["waterproof", "swimming", "shower", "water resistant", "ipx", "ip68"]):
            approved_water = specs.get("water_resistance") or specs.get("build", "")
            
            # Check if provider claimed 100% waterproof or safe for swimming when it's only IPX4
            if any(w in lower_text for w in ["100% waterproof", "swimming", "swimming pool", "submerge", "underwater"]):
                if "not suitable for swimming" in approved_water.lower() or "splash" in approved_water.lower():
                    claims.append({
                        "original_statement": provider_statement,
                        "timestamp": timestamp,
                        "segment_id": segment_id,
                        "category": "water_resistance",
                        "claim_text": "Device is suitable for swimming / completely waterproof",
                        "verification_status": "contradicted",
                        "supporting_source": f"{product['name']} Spec Sheet",
                        "supporting_excerpt": approved_water,
                        "explanation": "Device is only splash resistant (IPX4) and cannot be used for swimming.",
                        "corrected_text": f"The device is IPX4 splash resistant only and should not be submerged in water.",
                        "confidence": 0.98
                    })
            elif "ipx4" in lower_text or "splash" in lower_text:
                claims.append({
                    "original_statement": provider_statement,
                    "timestamp": timestamp,
                    "segment_id": segment_id,
                    "category": "water_resistance",
                    "claim_text": "Device is IPX4 splash resistant",
                    "verification_status": "verified",
                    "supporting_source": f"{product['name']} Spec Sheet",
                    "supporting_excerpt": approved_water,
                    "explanation": "Accurately described IPX4 splash resistance.",
                    "corrected_text": None,
                    "confidence": 0.95
                })

        # --- 3. Wireless Charging Claims ---
        if any(w in lower_text for w in ["wireless charging", "wireless charge", "वायरलेस चार्जिंग"]):
            approved_charging = specs.get("charging", "")
            if "wireless charging is not supported" in approved_charging.lower() or "not supported" in approved_charging.lower():
                if any(w in lower_text for w in ["does not support", "nahi hai", "not supported", "नहीं है", "नहीं मिलता"]):
                    claims.append({
                        "original_statement": provider_statement,
                        "timestamp": timestamp,
                        "segment_id": segment_id,
                        "category": "charging",
                        "claim_text": "Wireless charging not supported",
                        "verification_status": "verified",
                        "supporting_source": f"{product['name']} Spec Sheet",
                        "supporting_excerpt": approved_charging,
                        "explanation": "Accurately clarified absence of wireless charging.",
                        "corrected_text": None,
                        "confidence": 0.96
                    })
                elif any(w in lower_text for w in ["supports wireless", "has wireless", "can charge wirelessly", "bhi support karta hai", "सपोर्ट मिलता है"]):
                    claims.append({
                        "original_statement": provider_statement,
                        "timestamp": timestamp,
                        "segment_id": segment_id,
                        "category": "charging",
                        "claim_text": "Wireless charging supported",
                        "verification_status": "contradicted",
                        "supporting_source": f"{product['name']} Spec Sheet",
                        "supporting_excerpt": approved_charging,
                        "explanation": "Product does not support wireless charging.",
                        "corrected_text": "Wireless charging is not supported on this model; it uses fast wired charging.",
                        "confidence": 0.96
                    })

        # --- 4. Price & Discount Claims ---
        price_match = re.search(r"\b(?:rs|inr|rupees)?\s*(\d{1,2}(?:,\d{3})+|\d{4,6})\b", lower_text)
        if price_match and any(w in lower_text for w in ["price", "cost", "rupees", "rs", "inr", "discount", "एमआरपी", "कीमत", "डिस्काउंट", "रुपये", "दाम"]):
            claimed_price_num = int(price_match.group(1).replace(",", ""))
            approved_mrp_str = terms.get("mrp", "")
            approved_disc_str = terms.get("discounted_price", "")
            
            # Extract numbers from approved price
            approved_nums = [int(n.replace(",", "")) for n in re.findall(r"\b\d{1,2}(?:,\d{3})+|\d{4,6}\b", f"{approved_mrp_str} {approved_disc_str}")]
            
            if approved_nums:
                if claimed_price_num in approved_nums:
                    claims.append({
                        "original_statement": provider_statement,
                        "timestamp": timestamp,
                        "segment_id": segment_id,
                        "category": "pricing",
                        "claim_text": f"Price quoted: INR {claimed_price_num}",
                        "verification_status": "verified",
                        "supporting_source": f"{product['name']} Commercial Terms",
                        "supporting_excerpt": f"MRP: {approved_mrp_str}, Special Price: {approved_disc_str}",
                        "explanation": "Quoted price matches approved catalog pricing.",
                        "corrected_text": None,
                        "confidence": 0.97
                    })
                else:
                    claims.append({
                        "original_statement": provider_statement,
                        "timestamp": timestamp,
                        "segment_id": segment_id,
                        "category": "pricing",
                        "claim_text": f"Price quoted: INR {claimed_price_num}",
                        "verification_status": "contradicted",
                        "supporting_source": f"{product['name']} Commercial Terms",
                        "supporting_excerpt": f"MRP: {approved_mrp_str}, Special Price: {approved_disc_str}",
                        "explanation": f"Quoted INR {claimed_price_num}, whereas approved price is {approved_disc_str} (MRP: {approved_mrp_str}).",
                        "corrected_text": f"The verified price is {approved_disc_str} (MRP {approved_mrp_str}).",
                        "confidence": 0.95
                    })

        # --- 5. Camera Claims Extraction ---
        camera_match = re.search(r"(\d+)\s*(?:mp|megapixel|मेगापिक्सल|मेगापिक्सेल)", lower_text)
        if camera_match:
            claimed_mp = int(camera_match.group(1))
            approved_camera = specs.get("rear_camera") or specs.get("camera", "")
            approved_mp_nums = [int(n) for n in re.findall(r"\b(\d+)\s*mp\b", approved_camera.lower())]
            
            if approved_mp_nums:
                if claimed_mp in approved_mp_nums:
                    claims.append({
                        "original_statement": provider_statement,
                        "timestamp": timestamp,
                        "segment_id": segment_id,
                        "category": "camera",
                        "claim_text": f"{claimed_mp}MP camera sensor",
                        "verification_status": "verified",
                        "supporting_source": f"{product['name']} Spec Sheet",
                        "supporting_excerpt": approved_camera,
                        "explanation": f"Accurately quoted {claimed_mp}MP sensor matching approved specifications.",
                        "corrected_text": None,
                        "confidence": 0.98
                    })
                else:
                    claims.append({
                        "original_statement": provider_statement,
                        "timestamp": timestamp,
                        "segment_id": segment_id,
                        "category": "camera",
                        "claim_text": f"{claimed_mp}MP camera sensor",
                        "verification_status": "contradicted",
                        "supporting_source": f"{product['name']} Spec Sheet",
                        "supporting_excerpt": approved_camera,
                        "explanation": f"Claimed {claimed_mp}MP sensor, but official specification states: {approved_camera}.",
                        "corrected_text": f"The verified camera specification is: {approved_camera}.",
                        "confidence": 0.98
                    })

        return claims
