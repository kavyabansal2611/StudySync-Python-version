from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_ACCESS_SECRET: str
    JWT_REFRESH_SECRET: str
    JWT_EMAIL_SECRET: str
    JWT_PASSWORD_SECRET: str
    RESEND_API_KEY: str
    EMAIL_FROM: str
    FRONTEND_URL: str

    class Config:
        env_file = ".env"

settings=Settings()
