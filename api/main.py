"""
ProductGuard AI - FastAPI Application Entrypoint.
Multilingual Product Conversation Auditor & Coaching Engine.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.config import settings
from db.session import init_db
from api.routes import calls, products, providers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Database
    try:
        init_db()
    except Exception as e:
        print(f"Warning: Database initialization notice: {e}")
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Multilingual Product Conversation Auditor analyzing customer-service and sales conversations across English, Hindi, and Hinglish.",
    lifespan=lifespan
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(calls.router, prefix=settings.API_V1_PREFIX)
app.include_router(products.router, prefix=settings.API_V1_PREFIX)
app.include_router(providers.router, prefix=settings.API_V1_PREFIX)

@app.get("/", tags=["System"])
async def root():
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "documentation": "/docs",
        "supported_languages": ["English", "Hindi (Devanagari)", "Hinglish (Code-Switched)"]
    }

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "service": "ProductGuard AI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
