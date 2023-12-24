import asyncio
from utils.db import Base, engine
from utils import models  # don't delete this import


async def create_tables() -> None:
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    return

if __name__ == "__main__":
    asyncio.run(create_tables())
