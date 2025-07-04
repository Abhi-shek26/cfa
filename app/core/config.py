import os
from pydantic_settings import BaseSettings

# Ensure that the environment variables are loaded from the .env file
class Settings(BaseSettings):
    DATABASE_URL: str
    STOCK_DATA_PATH: str

    class Config:
        env_file = ".env"

settings = Settings()
print("--- Loaded Database URL:", settings.DATABASE_URL, "---")