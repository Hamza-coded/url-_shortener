from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .setting import settings


# Engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
)


# Session factory
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


# Base class for models
class Base(DeclarativeBase):
    pass


# Dependency
async def get_db():
    async with SessionLocal() as session:
        yield session