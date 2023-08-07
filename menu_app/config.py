import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_DB: str | None = os.getenv('POSTGRES_DB')
    POSTGRES_HOST: str | None = os.getenv('POSTGRES_HOST')
    POSTGRES_USER: str | None = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: str | None = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_PORT: str | None = os.getenv('POSTGRES_PORT')
    REDIS_PORT: str | None = os.getenv('REDIS_PORT')
    REDIS_HOST: str | None = os.getenv('REDIS_HOST')
    REDIS_DB: str | None = os.getenv('REDIS_DB')


settings = Settings()
