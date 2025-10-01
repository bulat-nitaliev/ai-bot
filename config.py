from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

class Settings(BaseSettings):
    BOT_TOKEN: str
    GIGACHAT_CREDENTIALS:str

    
    class Config:
        env_file = Path(".env")
        env_file_encoding = "utf-8"
        extra = "ignore"

# Создаём экземпляр настроек
settings = Settings()