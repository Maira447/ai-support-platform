import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    
    ENVIRONMENT: str = "development"
    MOCK_MODE: bool = True
    
    AGENT_API_KEY: str = "local-dev-key"
    
    VEEVO_API_BASE_URL: str = ""
    VEEVO_API_KEY: str = ""
    VEEVO_WHATSAPP_WEBHOOK_SECRET: str = ""
    VEEVO_WHATSAPP_PHONE_ID: str = ""
    
    REDIS_URL: str = ""
    DATABASE_URL: str = ""
    
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
