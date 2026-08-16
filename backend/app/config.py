import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "jobflow"
    JWT_SECRET: str = "your-super-secret-jwt-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    GEMINI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-flash-latest"
    FRONTEND_URL: str = "http://localhost:5173"

    class Config:
        env_file = ".env"

    @property
    def effective_gemini_api_key(self) -> str:
        return self.GEMINI_API_KEY or self.GOOGLE_API_KEY or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""


settings = Settings()
