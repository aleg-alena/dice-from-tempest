from abc import ABC
from typing import Any
from sqlalchemy import insert, update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert_or_ignore(self, pk: int) -> None:
        if not await self.exists(pk):
            await self.insert_one_pk(pk)
        return

    async def insert_one_data(self, data: dict[str, Any]) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self._session.execute(stmt)
        await self._session.commit()
        return res.scalar_one()

    async def insert_one(self) -> int:
        return await self.insert_one_data({})

    async def insert_one_pk(self, pk: int) -> int:
        return await self.insert_one_data({"id": pk})

    async def edit_all(self, data: dict[str, Any]) -> None:
        stmt = update(self.model).values(**data)
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def edit_where(self, filter_by: dict[str, Any], data: dict[str, Any]) -> None:
        stmt = update(self.model).values(**data).filter_by(**filter_by)
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def edit_one(self, pk: int, data: dict[str, Any]) -> None:
        await self.edit_where({"id": pk}, data)
        return

    async def select_one_where(self, filter_by: dict[str, Any]) -> Any:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self._session.execute(stmt)
        return res.scalar_one_or_none()

    async def select_many(self, filter_by: dict[str, Any]) -> Any:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self._session.execute(stmt)
        return res.scalars().all()

    async def select_all(self) -> Any:
        stmt = select(self.model)
        res = await self._session.execute(stmt)
        return res.scalars().all()

    async def select_one(self, pk: int) -> Any:
        return await self.select_one_where({"id": pk})

    async def exists_where(self, filter_by: dict[str, Any]) -> bool:
        stmt = select(self.model).filter_by(**filter_by)
        res = await self._session.execute(stmt)
        return res.fetchone() is not None

    async def exists(self, pk: int) -> bool:
        return await self.exists_where({"id": pk})

    async def delete_where(self, filter_by: dict[str, Any]) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        await self._session.execute(stmt)
        await self._session.commit()
        return

    async def delete_one(self, pk: int) -> None:
        await self.delete_where({"id": pk})
        return
    





