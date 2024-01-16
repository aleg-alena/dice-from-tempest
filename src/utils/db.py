from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from config import DB_URL

engine = create_async_engine(DB_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()
