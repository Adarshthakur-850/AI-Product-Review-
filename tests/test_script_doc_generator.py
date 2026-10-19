"""
Tests for Service Provider Compliance Script and Model Testing Doc Generator.
Verifies .docx and .md generation.
"""
import pytest
import os
from pathlib import Path
from services.script_doc_generator import ScriptDocGenerator
from services.knowledge_base import ProductKnowledgeBase

@pytest.fixture
def doc_generator(tmp_path):
    kb = ProductKnowledgeBase()
    return ScriptDocGenerator(kb=kb), tmp_path

def test_generate_docx_and_md(doc_generator):
    gen, tmp_dir = doc_generator
    
    # Generate for quantum-sound-pro
    docx_file = gen.generate_docx("quantum-sound-pro", output_dir=tmp_dir)
    md_file = gen.generate_markdown("quantum-sound-pro", output_dir=tmp_dir)
    
    assert docx_file.exists()
    assert docx_file.stat().st_size > 5000  # Valid docx size
    assert md_file.exists()
    
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    assert "Forbidden Statements" in content
    assert "Model Testing Benchmark Scenarios" in content
    assert "TEST-01" in content
