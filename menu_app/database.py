from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from menu_app.config import settings


def get_url():
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    hostname = settings.POSTGRES_HOST
    port = settings.POSTGRES_PORT
    db = settings.POSTGRES_DB

    return f'postgresql+asyncpg://{user}:{password}@{hostname}:{port}/{db}'


SQLALCHEMY_DATABASE_URL = get_url()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
