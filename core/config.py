from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_ACCESS_SECRET: str
    JWT_REFRESH_SECRET: str
    JWT_EMAIL_SECRET: str
    JWT_PASSWORD_SECRET: str
    RESEND_API_KEY: str
    EMAIL_FROM: str
    FRONTEND_URL: str
    EMAIL_VERIFICATION_EXPIRE_HOURS:int

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings()->Settings:
    return Settings()

settings=Settings()

