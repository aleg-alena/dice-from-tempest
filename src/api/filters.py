from aiogram.types import Message
from aiogram.filters import BaseFilter
from config import OWNERS


class IsOwner(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in OWNERS
