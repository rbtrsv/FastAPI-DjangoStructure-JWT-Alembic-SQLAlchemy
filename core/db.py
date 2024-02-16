# import os
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings

# Use the DATABASE_URL from settings directly.
# os.environ.get("DATABASE_URL")
DATABASE_URL = settings.DATABASE_URL

# Create an asynchronous engine for database connections.
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Function to create tables based on SQLModel models. This is intended to be run once.
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Function to get an async session for database operations. This is used with dependency injection in FastAPI.
async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session