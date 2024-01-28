from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import config

async_engine = create_async_engine(url=config.DB_URL)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)
