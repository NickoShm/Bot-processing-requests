from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import DB_URL
from data_base.create_models import Base


engine = create_async_engine(DB_URL)


session_maker = async_sessionmaker(engine)


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
