"""
SQLAlchemy database models for ProductGuard AI.
Covers Users, Providers, Products, Documents, Calls, Segments, Claims, Reports, and Audit Logs.
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Text, Float, Integer, Boolean, DateTime, ForeignKey, Enum as SQLEnum, JSON
)
from sqlalchemy.orm import relationship
from db.session import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class RoleEnum:
    CUSTOMER = "customer"
    PROVIDER = "provider"
    AUDITOR = "auditor"
    ADMIN = "admin"

class VerificationStatusEnum:
    VERIFIED = "verified"
    CONTRADICTED = "contradicted"
    UNSUPPORTED = "unsupported"
    AMBIGUOUS = "ambiguous"

class Provider(Base):
    __tablename__ = "providers"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    department = Column(String(100), default="Sales & Support")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    calls = relationship("Call", back_populates="provider", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String(50), primary_key=True)  # e.g., "quantum-sound-pro"
    name = Column(String(150), nullable=False)
    category = Column(String(100), nullable=False)
    brand = Column(String(100), default="QuantumTech")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    documents = relationship("ProductDocument", back_populates="product", cascade="all, delete-orphan")
    calls = relationship("Call", back_populates="product")

class ProductDocument(Base):
    __tablename__ = "product_documents"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    product_id = Column(String(50), ForeignKey("products.id"), nullable=False)
    title = Column(String(200), nullable=False)
    doc_type = Column(String(50), default="specification")  # spec, pricing, warranty, faq, policy
    content = Column(Text, nullable=False)
    version = Column(String(20), default="1.0")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    product = relationship("Product", back_populates="documents")

class Call(Base):
    __tablename__ = "calls"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    provider_id = Column(String(36), ForeignKey("providers.id"), nullable=False)
    product_id = Column(String(50), ForeignKey("products.id"), nullable=False)
    customer_name = Column(String(100), default="Customer")
    audio_path = Column(String(255), nullable=True)
    duration_seconds = Column(Float, default=0.0)
    primary_language = Column(String(20), default="Hinglish")
    disclosure_confirmed = Column(Boolean, default=True)
    status = Column(String(30), default="completed")  # pending, processing, completed, failed
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    provider = relationship("Provider", back_populates="calls")
    product = relationship("Product", back_populates="calls")
    segments = relationship("TranscriptSegment", back_populates="call", cascade="all, delete-orphan")
    claims = relationship("ExtractedClaim", back_populates="call", cascade="all, delete-orphan")
    report = relationship("CoachingReport", back_populates="call", uselist=False, cascade="all, delete-orphan")

class TranscriptSegment(Base):
    __tablename__ = "transcript_segments"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    call_id = Column(String(36), ForeignKey("calls.id"), nullable=False)
    speaker_role = Column(String(20), nullable=False)  # "customer" or "provider"
    start_time = Column(Float, default=0.0)
    end_time = Column(Float, default=0.0)
    text = Column(Text, nullable=False)
    detected_language = Column(String(20), default="en")  # "en", "hi", "hi-Latn"
    confidence = Column(Float, default=1.0)
    topic_category = Column(String(100), nullable=True)
    is_off_topic = Column(Boolean, default=False)
    
    call = relationship("Call", back_populates="segments")
    claims = relationship("ExtractedClaim", back_populates="segment")

class ExtractedClaim(Base):
    __tablename__ = "extracted_claims"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    call_id = Column(String(36), ForeignKey("calls.id"), nullable=False)
    segment_id = Column(String(36), ForeignKey("transcript_segments.id"), nullable=True)
    claim_text = Column(Text, nullable=False)
    category = Column(String(50), default="specification")  # battery, price, warranty, display, etc.
    verification_status = Column(String(30), default=VerificationStatusEnum.UNSUPPORTED)
    supporting_source = Column(String(200), nullable=True)
    supporting_excerpt = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    corrected_text = Column(Text, nullable=True)
    confidence = Column(Float, default=0.9)
    
    call = relationship("Call", back_populates="claims")
    segment = relationship("TranscriptSegment", back_populates="claims")

class CoachingReport(Base):
    __tablename__ = "coaching_reports"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    call_id = Column(String(36), ForeignKey("calls.id"), unique=True, nullable=False)
    
    # 100-Point Framework breakdown
    overall_score = Column(Float, default=0.0)
    relevance_score = Column(Float, default=0.0)
    accuracy_score = Column(Float, default=0.0)
    answer_quality_score = Column(Float, default=0.0)
    conciseness_score = Column(Float, default=0.0)
    clarity_score = Column(Float, default=0.0)
    
    summary = Column(Text, nullable=False)
    customer_questions = Column(JSON, default=list)
    missed_questions = Column(JSON, default=list)
    off_topic_segments = Column(JSON, default=list)
    action_recommendations = Column(JSON, default=list)
    language_feedback = Column(Text, nullable=True)
    deduction_details = Column(JSON, default=list)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    call = relationship("Call", back_populates="report")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_type = Column(String(50), nullable=False)  # call_ingested, report_generated, access_audited
    entity_id = Column(String(50), nullable=False)
    performed_by = Column(String(100), default="system")
    details = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
