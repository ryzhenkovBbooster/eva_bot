from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

# def create_async_engine(url: URL | str) -> AsyncEngine:
#     return create_engine(url=url, echo=True, encoding='utf-8', pool_pre_ping=True)

async def proceed_shemas(engine: AsyncEngine, metadata: MetaData)-> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession)

