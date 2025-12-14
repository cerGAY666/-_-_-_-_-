"""
Configuration module for Pulse AI Assistant.
Loads settings from environment variables and YAML config.
"""
import os
from pathlib import Path
from typing import Optional
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # Database
    DB_URI: str = os.getenv("DB_URI", "postgresql://postgres:zov@localhost:5432/db")
    
    # LM Studio
    LM_STUDIO_BASE_URL: str = os.getenv("LM_STUDIO_BASE_URL", "http://127.0.0.1:1234/v1")
    LM_STUDIO_API_KEY: str = os.getenv("LM_STUDIO_API_KEY", "lm-studio")
    
    # Embeddings
    EMBEDDINGS_MODEL: str = os.getenv("EMBEDDINGS_MODEL", "all-MiniLM-L6-v2")
    EMBEDDINGS_CACHE_PATH: Path = Path(os.getenv("EMBEDDINGS_CACHE_PATH", "./data/processed/embeddings_cache"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Path = Path(os.getenv("LOG_FILE", "./logs/app.log"))
    
    # Application
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        if not cls.DB_URI:
            raise ValueError("DB_URI is required")
        
        # Create directories if they don't exist
        cls.EMBEDDINGS_CACHE_PATH.mkdir(parents=True, exist_ok=True)
        cls.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Global config instance
config = Config()
