import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Task Management Platform"
    DEBUG: bool = True
    

    
                    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6379"
    
              
    TELEGRAM_BOT_TOKEN: str = "MOCK_TOKEN"
    TELEGRAM_WEBHOOK_URL: Optional[str] = None
    
            
    GROQ_API_KEY: str = "MOCK_GROQ_KEY"
    
                                      
    ACTIVE_PROVIDER: str = "mock"                               
    PLANE_API_KEY: Optional[str] = None
    PLANE_WORKSPACE_SLUG: Optional[str] = None
    PLANE_PROJECT_ID: Optional[str] = None
    
    LINEAR_API_KEY: Optional[str] = None
    LINEAR_TEAM_ID: Optional[str] = None
    
                                 # AI and Extraction Settings
    CONFIDENCE_THRESHOLD: float = 0.85
    
    # Telegram Developer Mapping (Name -> Chat ID)
    DEV_TELEGRAM_IDS: dict[str, int] = {}
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    
    
    @property
    def celery_broker_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"
        
    @property
    def celery_result_backend(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/1"

settings = Settings()
