"""
Sentinel AI - Configuration Module
Loads environment variables and provides app-wide settings.
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    gemini_api_key: str = "<GEMINI_API_KEY>"
    api_secret_key: str = "<API_SECRET_KEY>"
    object_storage_key: str = "<OBJECT_STORAGE_KEY>"
    object_storage_secret: str = "<OBJECT_STORAGE_SECRET>"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Upload settings
    max_upload_size_mb: int = 50
    upload_dir: Path = Path("/tmp/uploads")
    file_retention_seconds: int = 300
    
    # Application
    debug: bool = False
    cors_origins: str = "http://localhost:3000,http://localhost:8080"
    
    # Content limits
    max_text_length: int = 10000
    max_audio_duration_seconds: int = 30
    max_video_duration_seconds: int = 8
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()

# Ensure upload directory exists
settings.upload_dir.mkdir(parents=True, exist_ok=True)
