"""
Service Provider Talk-Track and Model Testing Guide Generator.
Generates comprehensive Word (.docx) and Markdown (.md) documents
specifying compliant customer dialogues, forbidden claims, and model testing benchmarks.
"""
from pathlib import Path
from typing import Dict, Any, Optional
import json
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from services.knowledge_base import ProductKnowledgeBase
from core.config import settings

class ScriptDocGenerator:
    """
    Generates standardized compliance guidebooks and model testing benchmark documents.
    """
    def __init__(self, kb: Optional[ProductKnowledgeBase] = None):
        self.kb = kb or ProductKnowledgeBase()

    def generate_docx(self, product_id: str, output_dir: Optional[Path] = None) -> Path:
        """
        Creates a professional .docx document for service providers and model testing.
        """
        product = self.kb.get_product(product_id)
        if not product:
            raise ValueError(f"Product '{product_id}' not found in approved catalog.")

        out_dir = output_dir or (settings.BASE_DIR / "generated_docs")
        out_dir.mkdir(parents=True, exist_ok=True)
        docx_path = out_dir / f"{product_id}_compliance_script_guide.docx"

        doc = docx.Document()

        # Set standard margins
        for section in doc.sections:
            section.top_margin = Inches(0.8)
            section.bottom_margin = Inches(0.8)
            section.left_margin = Inches(0.8)
            section.right_margin = Inches(0.8)

        # Document Title
        title_p = doc.add_paragraph()
        title_p.paragraph_format.space_before = Pt(0)
        title_p.paragraph_format.space_after = Pt(4)
        run_title = title_p.add_run("ProductGuard AI — Compliance & Talk-Track Guide")
        run_title.font.size = Pt(20)
        run_title.font.bold = True
        run_title.font.color.rgb = RGBColor(30, 41, 59)

        subtitle_p = doc.add_paragraph()
        subtitle_p.paragraph_format.space_after = Pt(16)
        run_sub = subtitle_p.add_run(f"Standard Service Provider Operating Script & Model Testing Benchmark for {product['name']}")
        run_sub.font.size = Pt(11)
        run_sub.font.italic = True
        run_sub.font.color.rgb = RGBColor(100, 116, 139)

        # 1. Product Metadata Table
        doc.add_heading("1. Product Overview & Version Metadata", level=1)
        table = doc.add_table(rows=5, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.style = "Table Grid"

        meta_rows = [
            ("Product Name", product.get("name", "")),
            ("Product Category", product.get("category", "")),
            ("Brand", product.get("brand", "")),
            ("Catalog Version", f"v{product.get('version', '1.0')} (Approved {product.get('approved_date', '2026')})"),
            ("Intended Audience", "Service Providers, Sales Representatives, Quality Auditors & AI Testers")
        ]
        for idx, (label, val) in enumerate(meta_rows):
            cell_lbl, cell_val = table.rows[idx].cells
            cell_lbl.text = label
            cell_lbl.paragraphs[0].runs[0].font.bold = True
            cell_val.text = val

        doc.add_paragraph()

        # 2. Golden Rules for Service Providers
        doc.add_heading("2. Mandatory Service Provider Rules of Engagement", level=1)
        doc.add_paragraph("Service providers MUST strictly adhere to the following 5 compliance pillars during every conversation:")
        
        rules = [
            ("Strict Factual Grounding", "Quote ONLY verified specifications from approved catalog sheets. Never guess or inflate specs."),
            ("Conversational Relevance", "Answer the customer's question directly. Strictly avoid personal anecdotes (e.g., vacations, family stories, friends)."),
            ("Answer Completeness & Clarity", "Address the customer's explicit inquiry before pivoting to another feature."),
            ("Paced Conciseness", "Keep each turn under 40 words. Pause and allow the customer to ask follow-up questions."),
            ("Multilingual Respect", "Fluently support English, Hindi, or Hinglish without dropping or distorting official technical terminology.")
        ]
        for title, desc in rules:
            p = doc.add_paragraph(style="List Bullet")
            r_bold = p.add_run(f"{title}: ")
            r_bold.font.bold = True
            p.add_run(desc)

        doc.add_paragraph()

        # 3. Approved Multilingual Dialogue Script
        doc.add_heading("3. Approved Multilingual Talk-Track Scripts", level=1)
        doc.add_paragraph("Follow these exact verified talk-tracks across English, Hindi, and Hinglish modes:")

        specs = product.get("specifications", {})
        terms = product.get("commercial_terms", {})
        policies = product.get("policies", {})

        # Script Table
        script_table = doc.add_table(rows=1, cols=3)
        script_table.style = "Table Grid"
        hdr_cells = script_table.rows[0].cells
        hdr_cells[0].text = "Customer Question / Topic"
        hdr_cells[1].text = "Approved Talk-Track (Hinglish / Hindi)"
        hdr_cells[2].text = "Approved Talk-Track (English)"
        for cell in hdr_cells:
            cell.paragraphs[0].runs[0].font.bold = True

        dialogues = [
            (
                "Greeting & Opening",
                "Namaste sir, welcome! Main is product ke specifications me aapki kya sahayata kar sakta hu?",
                "Hello, welcome! How can I assist you with this product's specifications today?"
            ),
            (
                "Battery Runtime Inquiry",
                f"Sir, iska verified battery backup {specs.get('battery_life', specs.get('battery', ''))} hai.",
                f"The verified battery runtime provides {specs.get('battery_life', specs.get('battery', ''))}."
            ),
            (
                "Charging Capabilities",
                f"Isme {specs.get('charging', '')} support milta hai.",
                f"It features {specs.get('charging', '')}."
            ),
            (
                "Pricing & Launch Offers",
                f"Sir iska MRP {terms.get('mrp', '')} hai, aur offer me ye {terms.get('discounted_price', '')} me available hai.",
                f"The official price is {terms.get('discounted_price', '')} (MRP: {terms.get('mrp', '')})."
            ),
            (
                "Warranty & Return Terms",
                f"Is par {policies.get('warranty', '')} milti hai.",
                f"It includes a {policies.get('warranty', '')}."
            )
        ]
        for q, hi_track, en_track in dialogues:
            row_cells = script_table.add_row().cells
            row_cells[0].text = q
            row_cells[0].paragraphs[0].runs[0].font.bold = True
            row_cells[1].text = hi_track
            row_cells[2].text = en_track

        doc.add_paragraph()

        # 4. Critical Forbidden Statements (What NOT to say)
        doc.add_heading("4. ⛔ FORBIDDEN CLAIMS (Strict Violations)", level=1)
        doc.add_paragraph("Making any of the following claims will result in immediate compliance failure (-10 pts each):")

        forbidden_p = doc.add_paragraph(style="List Bullet")
        f_run1 = forbidden_p.add_run("FALSE WATERPROOF CLAIMS: ")
        f_run1.font.bold = True
        f_run1.font.color.rgb = RGBColor(220, 38, 38)
        forbidden_p.add_run(f"Never claim the product is 100% waterproof for swimming unless officially rated for submersion. Current rating: {specs.get('water_resistance', specs.get('build', 'Splash resistant only'))}.")

        forbidden_p2 = doc.add_paragraph(style="List Bullet")
        f_run2 = forbidden_p2.add_run("FALSE WIRELESS CHARGING CLAIMS: ")
        f_run2.font.bold = True
        f_run2.font.color.rgb = RGBColor(220, 38, 38)
        forbidden_p2.add_run("Never claim wireless charging is supported if the catalog states wired charging only.")

        forbidden_p3 = doc.add_paragraph(style="List Bullet")
        f_run3 = forbidden_p3.add_run("PERSONAL ANECDOTES & STORIES: ")
        f_run3.font.bold = True
        f_run3.font.color.rgb = RGBColor(220, 38, 38)
        forbidden_p3.add_run("Never discuss personal holidays, trips with friends, or unrelated family anecdotes.")

        forbidden_p4 = doc.add_paragraph(style="List Bullet")
        f_run4 = forbidden_p4.add_run("INVENTED SPECIFICATIONS: ")
        f_run4.font.bold = True
        f_run4.font.color.rgb = RGBColor(220, 38, 38)
        forbidden_p4.add_run("If a specification is missing from the catalog, say 'I will verify that with our technical team' rather than inventing numbers.")

        doc.add_paragraph()

        # 5. Model Testing Scenarios & Expected Auditor Output
        doc.add_heading("5. Model Testing Benchmark Scenarios", level=1)
        doc.add_paragraph("Use these structured test cases to evaluate and benchmark the ProductGuard AI Auditor:")

        test_table = doc.add_table(rows=1, cols=4)
        test_table.style = "Table Grid"
        t_hdr = test_table.rows[0].cells
        t_hdr[0].text = "Test ID & Scenario"
        t_hdr[1].text = "Input Statement"
        t_hdr[2].text = "Expected Auditor Classification"
        t_hdr[3].text = "Expected Score Impact"
        for c in t_hdr:
            c.paragraphs[0].runs[0].font.bold = True

        tests_data = [
            (
                "TEST-01 (Ideal Compliant)",
                f"Battery backup is {specs.get('battery_life', specs.get('battery', ''))}.",
                "Category: direct_answer\nStatus: VERIFIED",
                "0 pts deduction (100% score)"
            ),
            (
                "TEST-02 (Contradiction)",
                "This device is 100% waterproof for deep swimming.",
                "Category: misleading_statement\nStatus: CONTRADICTED",
                "-10 pts deduction (Factual Accuracy)"
            ),
            (
                "TEST-03 (Off-Topic Tangent)",
                "My friend bought this when we went on our Goa trip last month.",
                "Category: off_topic_personal_discussion\nIs_Off_Topic: True",
                "-6 pts deduction (Product Relevance)"
            ),
            (
                "TEST-04 (Repetitive Elaboration)",
                "Repeating the same battery runtime three times consecutively.",
                "Category: repetition_unnecessary_elaboration",
                "-4 pts deduction (Conciseness)"
            )
        ]
        for tid, stmt, exp_cls, score_imp in tests_data:
            r = test_table.add_row().cells
            r[0].text = tid
            r[0].paragraphs[0].runs[0].font.bold = True
            r[1].text = stmt
            r[2].text = exp_cls
            r[3].text = score_imp

        # Save document
        doc.save(str(docx_path))
        return docx_path

    def generate_markdown(self, product_id: str, output_dir: Optional[Path] = None) -> Path:
        """
        Creates a markdown version of the compliance guide for immediate in-browser reading.
        """
        product = self.kb.get_product(product_id)
        if not product:
            raise ValueError(f"Product '{product_id}' not found.")

        out_dir = output_dir or (settings.BASE_DIR / "generated_docs")
        out_dir.mkdir(parents=True, exist_ok=True)
        md_path = out_dir / f"{product_id}_compliance_script_guide.md"

        specs = product.get("specifications", {})
        terms = product.get("commercial_terms", {})
        policies = product.get("policies", {})

        content = f"""# ProductGuard AI — Service Provider Talk-Track & Model Testing Guide
**Product:** {product['name']} ({product.get('category')})  
**Brand:** {product.get('brand')} | **Catalog Version:** v{product.get('version', '1.0')}  

---

## 1. Mandatory Service Provider Rules of Engagement
1. **Strict Factual Grounding**: Quote ONLY verified specifications from approved catalog sheets. Never guess.
2. **Conversational Relevance**: Answer the customer's question directly. Strictly avoid personal anecdotes (vacations, friends, family).
3. **Paced Conciseness**: Keep each turn under 40 words. Allow customer follow-ups.
4. **Multilingual Fluidity**: Accurately converse in English, Hindi, or Hinglish while preserving technical terms.

---

## 2. Approved Multilingual Talk-Track Scripts

| Customer Question / Topic | Approved Talk-Track (Hinglish / Hindi) | Approved Talk-Track (English) |
| :--- | :--- | :--- |
| **Greeting** | Namaste sir, welcome! Main is product ke specifications me aapki kya sahayata kar sakta hu? | Hello, welcome! How can I assist you with this product's specifications today? |
| **Battery Life** | Sir, iska verified battery backup {specs.get('battery_life', specs.get('battery', ''))} hai. | The verified battery runtime provides {specs.get('battery_life', specs.get('battery', ''))}. |
| **Charging** | Isme {specs.get('charging', '')} support milta hai. | It features {specs.get('charging', '')}. |
| **Price & Offers** | Sir iska MRP {terms.get('mrp', '')} hai, aur offer me ye {terms.get('discounted_price', '')} me available hai. | The official price is {terms.get('discounted_price', '')} (MRP: {terms.get('mrp', '')}). |
| **Warranty** | Is par {policies.get('warranty', '')} milti hai. | It includes a {policies.get('warranty', '')}. |

---

## 3. ⛔ Forbidden Statements (Strict Compliance Violations)
- ❌ **False Waterproof Claims**: Never claim the device is swimming-safe unless approved. Rating is: `{specs.get('water_resistance', specs.get('build', 'Splash resistant only'))}`.
- ❌ **False Wireless Charging Claims**: Never claim wireless charging if catalog states wired fast charging only.
- ❌ **Personal Anecdotes**: Never discuss personal trips or friends.
- ❌ **Uncataloged Assertions**: If info is missing, say *"I will verify that with our technical catalog"* rather than inventing specs.

---

## 4. Model Testing Benchmark Scenarios

| Test ID | Test Utterance | Expected Auditor Evaluation | Expected Score Impact |
| :--- | :--- | :--- | :--- |
| **TEST-01 (Compliant)** | *"Battery backup is {specs.get('battery_life', specs.get('battery', ''))}."* | Category: `direct_answer`, Status: `VERIFIED` | 0 pts deduction (100% score) |
| **TEST-02 (Contradiction)** | *"This device is 100% waterproof for deep swimming."* | Category: `misleading_statement`, Status: `CONTRADICTED` | -10 pts deduction |
| **TEST-03 (Off-Topic)** | *"My friend bought this when we went on our Goa trip last month."* | Category: `off_topic_personal_discussion`, Is_Off_Topic: `True` | -6 pts deduction |
| **TEST-04 (Repetition)** | *Repeats battery claim 3 times consecutively.* | Category: `repetition_unnecessary_elaboration` | -4 pts deduction |
"""
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(content)

        return md_path
