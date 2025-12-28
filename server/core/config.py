"""
Antigravity AI - Configuration Management
Centralized settings with Pydantic BaseSettings
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Antigravity AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str
    
    # Redis / Celery
    REDIS_URL: str
    
    # MinIO / S3
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str = "antigravity-videos"
    MINIO_USE_SSL: bool = False
    
    # AI Model Paths
    LIVEPORTRAIT_WEIGHTS: str = "/weights/liveportrait"
    GFPGAN_WEIGHTS: str = "/weights/gfpgan/GFPGANv1.4.pth"
    
    # GPU Configuration
    CUDA_VISIBLE_DEVICES: str = "0"
    PYTORCH_CUDA_ALLOC_CONF: str = "max_split_size_mb:512"
    
    # Audio Synthesis - FREE HIGH QUALITY
    USE_EDGE_TTS: bool = True
    USE_COQUI_TTS: bool = True
    COQUI_MODEL: str = "tts_models/multilingual/multi-dataset/xtts_v2"
    
    # Optional Premium (ElevenLabs)
    ELEVENLABS_API_KEY: Optional[str] = None
    
    # Hugging Face Token (for Spaces)
    HF_TOKEN: Optional[str] = None
    
    # Voice Configuration - BEST FREE VOICES
    # Edge-TTS Neural Voices (90% premium quality)
    VOICE_ARCHETYPES: dict = {
        "philosopher": {
            "engine": "edge-tts",
            "voice": "en-US-GuyNeural",  # Deep, resonant male
            "rate": "-10%",
            "pitch": "-5Hz"
        },
        "storyteller": {
            "engine": "edge-tts",
            "voice": "hi-IN-SwaraNeural",  # Warm Hindi/English
            "rate": "+0%",
            "pitch": "+0Hz"
        },
        "innovator": {
            "engine": "edge-tts",
            "voice": "en-US-AriaNeural",  # Sharp, clear female
            "rate": "+10%",
            "pitch": "+3Hz"
        },
        "narrator_male": {
            "engine": "edge-tts",
            "voice": "en-GB-RyanNeural",  # British male
            "rate": "+0%",
            "pitch": "+0Hz"
        },
        "narrator_female": {
            "engine": "edge-tts",
            "voice": "en-GB-SoniaNeural",  # British female
            "rate": "+0%",
            "pitch": "+0Hz"
        },
        "indian_english": {
            "engine": "edge-tts",
            "voice": "en-IN-NeerjaNeural",  # Indian English female
            "rate": "+0%",
            "pitch": "+0Hz"
        }
    }
    
    DEFAULT_VOICE_MALE: str = "en-US-GuyNeural"
    DEFAULT_VOICE_FEMALE: str = "en-US-AriaNeural"
    DEFAULT_VOICE_HINDI: str = "hi-IN-SwaraNeural"
    
    # Feature Flags
    ENABLE_LANDMARK_PREVIEW: bool = True
    ENABLE_QUALITY_METRICS: bool = True
    MAX_VIDEO_DURATION: int = 60  # seconds
    
    # Security
    JWT_SECRET: str
    CORS_ORIGINS: str = "http://localhost:3000,https://ai.technoamaze.in,https://technoamaze.in"
    
    # Performance Tuning
    MAX_WORKERS: int = 4
    CELERY_TASK_TIMEOUT: int = 600  # 10 minutes
    GPU_MEMORY_FRACTION: float = 0.8
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_voice_config(archetype: str = "narrator_male") -> dict:
    """Get voice configuration for specific archetype"""
    return settings.VOICE_ARCHETYPES.get(
        archetype, 
        settings.VOICE_ARCHETYPES["narrator_male"]
    )


def get_language_voice(language_code: str) -> str:
    """Auto-select voice based on detected language"""
    language_map = {
        "hi": settings.DEFAULT_VOICE_HINDI,
        "en": settings.DEFAULT_VOICE_MALE,
        "en-IN": "en-IN-NeerjaNeural",
        "en-GB": "en-GB-RyanNeural",
        "en-US": settings.DEFAULT_VOICE_MALE,
    }
    return language_map.get(language_code, settings.DEFAULT_VOICE_MALE)
