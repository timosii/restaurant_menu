from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    TESTING: bool
    TEST_DB_NAME: str
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
