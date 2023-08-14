import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_DB = os.getenv('REDIS_DB')
    RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER')
    RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS')
    RABBITMQ_DEFAULT_HOST = os.getenv('RABBITMQ_DEFAULT_HOST')
    RABBITMQ_DEFAULT_PORT = os.getenv('RABBITMQ_DEFAULT_PORT')


settings = Settings()
