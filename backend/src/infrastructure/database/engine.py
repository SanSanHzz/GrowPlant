from os import getenv

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://growplant:growplant_dev@postgres:5432/growplant",
)


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL, echo=False)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
