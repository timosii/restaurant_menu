import os

from dotenv import load_dotenv

load_dotenv('./.env_local')


class Settings:
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_DB = os.getenv('REDIS_DB')


settings = Settings()
