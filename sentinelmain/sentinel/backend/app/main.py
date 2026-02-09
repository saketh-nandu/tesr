"""
Sentinel AI - FastAPI Main Application
Entry point for the backend API.
"""
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import text, audio, image, video
from app.utils.file_handler import cleanup_old_files


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Handles startup and shutdown events.
    """
    # Startup: Initialize resources
    print("🚀 Sentinel AI starting up...")
    print(f"📁 Upload directory: {settings.upload_dir}")
    
    # Start background cleanup task
    cleanup_task = asyncio.create_task(periodic_cleanup())
    
    yield
    
    # Shutdown: Cleanup resources
    print("👋 Sentinel AI shutting down...")
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass


async def periodic_cleanup():
    """Periodically clean up old uploaded files."""
    while True:
        await asyncio.sleep(60)  # Run every minute
        cleanup_old_files()


# Create FastAPI application
app = FastAPI(
    title="Sentinel AI",
    description="AI-powered content analysis for detecting deepfakes and scams",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(text.router, prefix="/analyze", tags=["Analysis"])
app.include_router(audio.router, prefix="/analyze", tags=["Analysis"])
app.include_router(image.router, prefix="/analyze", tags=["Analysis"])
app.include_router(video.router, prefix="/analyze", tags=["Analysis"])


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker."""
    return {"status": "healthy", "service": "sentinel-ai"}


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Sentinel AI",
        "version": "1.0.0",
        "description": "Check if content is AI-generated or a scam",
        "endpoints": {
            "text": "POST /analyze/text",
            "audio": "POST /analyze/audio",
            "image": "POST /analyze/image",
            "video": "POST /analyze/video"
        }
    }
