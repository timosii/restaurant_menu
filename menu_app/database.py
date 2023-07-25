import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def get_url():
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "123")
    server = os.getenv("POSTGRES_SERVER", "localhost")
    db = os.getenv("POSTGRES_DB", "menu_db")
    return f"postgresql://{user}:{password}@{server}/{db}"

SQLALCHEMY_DATABASE_URL = get_url()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

