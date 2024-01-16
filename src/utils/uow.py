from typing_extensions import Self, Any
from utils.db import async_session_maker
from utils.repositories import UsersRepository, DiceRoomsRepository


class UnitOfWork:
    async def __aenter__(self) -> Self:
        self.session = async_session_maker()

        self.users = UsersRepository(self.session)
        self.dice_rooms = DiceRoomsRepository(self.session)

        return self

    async def __aexit__(self, exc_type: Exception, *args: Any) -> None:
        if exc_type is None:
            await self.commit()
        await self.session.close()
        return

    async def commit(self) -> None:
        await self.session.commit()
        return
