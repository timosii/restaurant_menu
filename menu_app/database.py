from .config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import Depends
from typing_extensions import Annotated


def get_url():
    if settings.TESTING:
        db = settings.TEST_DB_NAME
    else:
        db = settings.POSTGRES_DB
    
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    hostname = settings.POSTGRES_HOST
    port = settings.POSTGRES_PORT
        
    return f"postgresql://{user}:{password}@{hostname}:{port}/{db}"


SQLALCHEMY_DATABASE_URL = get_url()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
