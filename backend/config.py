import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Configuration
    APP_NAME: str = "AI Coding Interview Coach Pro"
    VERSION: str = "2.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ai_coach.db")
    
    # AI Services
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Evaluation Settings
    MAX_CODE_LENGTH: int = 10000
    ALLOWED_LANGUAGES: List[str] = ["python", "javascript", "java", "cpp", "go"]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    # Analytics
    ENABLE_ANALYTICS: bool = True
    ANALYTICS_RETENTION_DAYS: int = 90
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()