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

# from pydantic_settings import BaseSettings # вероятно проблема в этом
# from pydantic import field_validator, BaseModel
# from dotenv import load_dotenv

# load_dotenv()

# class Settings(BaseSettings):
#     POSTGRES_USER: str
#     POSTGRES_PASSWORD: str
#     POSTGRES_HOST: str
#     POSTGRES_PORT: int
#     POSTGRES_DB: str
#     TESTING: bool
#     TEST_DB_NAME: str

#     @field_validator("POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_DB", "TESTING", "TEST_DB_NAME")
#     def check_config(cls, values):
#         # Здесь вы можете добавить свою проверку значений, если нужно
#         return values

settings = Settings()
