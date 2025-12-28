"""
Antigravity AI - FastAPI Application
Main server entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging

from core.config import settings
from routers import v1_generation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-grade Talking Head Reality Engine - Defy Gravity"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(v1_generation.router, prefix="/api/v1", tags=["generation"])

# Mount static files for local storage (Bypass MinIO)
from pathlib import Path
TEMP_DIR = Path("/tmp/antigravity")
TEMP_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static/generated", StaticFiles(directory=str(TEMP_DIR)), name="generated")


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting...")
    logger.info(f"   Device: {'CUDA' if settings.CUDA_VISIBLE_DEVICES else 'CPU'}")
    logger.info(f"   Edge-TTS: {'Enabled' if settings.USE_EDGE_TTS else 'Disabled'}")
    logger.info(f"   Coqui TTS: {'Enabled' if settings.USE_COQUI_TTS else 'Disabled'}")
    
    # Preload AI models (optional - saves time on first request)
    # from engines import audio_synthesizer, animator, enhancer
    # animator.load_model()
    # enhancer.load_model()

    # Initialize Avatar Generator (creates gallery dir)
    from engines.avatar_generator import avatar_generator
    # avatar_generator._load_avatar_catalog() # Already called in __init__
    
    logger.info("✓ Startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down...")
    
    # Clear GPU memory
    from engines import animator, enhancer
    animator.clear_gpu_memory()
    enhancer.clear_gpu_memory()
    
    logger.info("✓ Shutdown complete")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "message": "Defy Gravity - The Talking Head Reality Engine"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    import torch
    
    return {
        "status": "healthy",
        "cuda_available": torch.cuda.is_available(),
        "cuda_devices": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "edge_tts": settings.USE_EDGE_TTS,
        "coqui_tts": settings.USE_COQUI_TTS,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
