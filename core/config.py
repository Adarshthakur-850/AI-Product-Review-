"""
ProductGuard AI - Core Configuration & Settings.
"""
from pathlib import Path
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseModel, ConfigDict
    class BaseSettings(BaseModel):
        model_config = ConfigDict(extra="allow")

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "ProductGuard AI"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Paths
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"
    CATALOG_DIR: Path = BASE_DIR / "data" / "catalog"
    CONVERSATIONS_DIR: Path = BASE_DIR / "data" / "sample_conversations"
    STORAGE_DIR: Path = BASE_DIR / "storage"
    
    # Database (Default SQLite for portability, switchable to PostgreSQL)
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'productguard.db'}"
    
    # NLP & Embedding Models
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    # 100-Point Scoring Framework Weights
    SCORE_FACTUAL_ACCURACY: float = 30.0
    SCORE_PRODUCT_RELEVANCE: float = 25.0
    SCORE_ANSWER_QUALITY: float = 20.0
    SCORE_CONCISENESS: float = 15.0
    SCORE_COMMUNICATION_CLARITY: float = 10.0
    
    # Deductions
    DEDUCTION_CONTRADICTED_CLAIM: float = 10.0
    DEDUCTION_UNSUPPORTED_ASSERTION: float = 5.0
    DEDUCTION_OFF_TOPIC_STORY: float = 6.0
    DEDUCTION_CIRCULAR_REPETITION: float = 4.0
    DEDUCTION_MISSED_QUESTION: float = 8.0
    
    # Retention & Safety Policy
    RETENTION_DAYS: int = 90
    REQUIRE_RECORDING_DISCLOSURE: bool = True
    
    model_config = ConfigDict(extra="allow")

settings = Settings()
