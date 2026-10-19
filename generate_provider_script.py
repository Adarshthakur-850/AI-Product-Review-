"""
Command-Line Script to Generate Service Provider Compliance Script (.docx and .md).
Used by service providers to follow compliant talk-tracks and QA testers for model benchmarking.
"""
import sys
import argparse
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from services.script_doc_generator import ScriptDocGenerator
from services.knowledge_base import ProductKnowledgeBase

def main():
    parser = argparse.ArgumentParser(
        description="Generate Service Provider Talk-Track & Model Testing Guide (.docx & .md)"
    )
    parser.add_argument(
        "product_id",
        nargs="?",
        default="quantum-sound-pro",
        help="Product ID slug from approved catalog (e.g. quantum-sound-pro, apex-phone-15)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate compliance doc scripts for ALL products in the catalog"
    )
    args = parser.parse_args()

    kb = ProductKnowledgeBase()
    generator = ScriptDocGenerator(kb=kb)

    products_to_generate = []
    if args.all:
        products_to_generate = [p["id"] for p in kb.list_products()]
    else:
        products_to_generate = [args.product_id]

    print("=" * 70)
    print(" ProductGuard AI — Service Provider Talk-Track & Model Testing Doc Generator")
    print("=" * 70)

    for pid in products_to_generate:
        try:
            print(f"\n[+] Generating compliance script for product: '{pid}' ...")
            docx_path = generator.generate_docx(pid)
            md_path = generator.generate_markdown(pid)
            print(f"    ✔ Word Document (.docx): {docx_path}")
            print(f"    ✔ Markdown Guide (.md):  {md_path}")
        except Exception as e:
            print(f"    ❌ Error generating script for '{pid}': {e}")

    print("\n✅ Document generation complete! Files saved in 'generated_docs/' folder.")

if __name__ == "__main__":
    main()
