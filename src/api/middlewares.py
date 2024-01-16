from typing import Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import Message
from utils.uow import UnitOfWork


class UOWSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message, data: dict[str, Any]) -> Any:

        async with UnitOfWork() as uow:
            await uow.users.insert_or_ignore(event.from_user.id)
            data['uow'] = uow

            return await handler(event, data)
