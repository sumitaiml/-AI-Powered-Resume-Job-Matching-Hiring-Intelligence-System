"""
Main FastAPI Application
HRTech Platform - AI-powered resume screening and candidate ranking
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.core import settings, DatabaseManager
from app.apis import candidates, jobs, ranking

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database
DatabaseManager.initialize()
DatabaseManager.create_all_tables()

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(candidates.router)
app.include_router(jobs.router)
app.include_router(ranking.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "HRTech Platform API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "hrtech-platform",
        "version": settings.API_VERSION
    }


@app.get("/api/config")
async def get_config():
    """Get system configuration (public, non-sensitive info)"""
    return {
        "api_title": settings.API_TITLE,
        "api_version": settings.API_VERSION,
        "features": {
            "bias_mitigation": settings.APPLY_BIAS_MITIGATION,
            "explainability": True,
            "skill_graph_inference": True
        },
        "ranking_weights": {
            "skill_weight": settings.SKILL_WEIGHT,
            "experience_weight": settings.EXPERIENCE_WEIGHT,
            "seniority_weight": settings.SENIORITY_WEIGHT
        }
    }


def custom_openapi():
    """Custom OpenAPI schema"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.API_TITLE,
        version=settings.API_VERSION,
        description=settings.API_DESCRIPTION,
        routes=app.routes,
    )
    
    openapi_schema["info"]["x-logo"] = {
        "url": "https://hrtech-platform.com/logo.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Event handlers
@app.on_event("startup")
async def startup():
    """Startup event"""
    logger.info("🚀 HRTech Platform backend starting...")
    logger.info(f"📊 Database: {settings.DATABASE_URL}")
    logger.info(f"🧠 NLP Model: {settings.SPACY_MODEL}")
    logger.info(f"🎯 SBERT Model: {settings.SBERT_MODEL}")
    logger.info("✅ Backend ready!")


@app.on_event("shutdown")
async def shutdown():
    """Shutdown event"""
    logger.info("👋 HRTech Platform backend shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
