from typing import Any
from utils.abstract_repository import AbstractRepository
from utils.models.users import Users


class UsersRepository(AbstractRepository):
    model = Users

    async def select_by_rr_acc(self, rr_acc: int) -> Users:
        return await self.select_one_where({"rr_acc": rr_acc})

    async def set_rr_acc(self, user_id: int, rr_acc: int) -> None:
        await self.edit_one(user_id, {"rr_acc": rr_acc})
        return

    async def set_cash(self, user_id: int, amount: Any) -> None:
        await self.edit_one(user_id, {"cash": amount})
        return

    async def set_Lang(self, user_id: int, amount: Any) -> None:
        await self.edit_one(user_id, {"Lang": amount})
        return

    async def add_cash(self, user_id: int, amount: int) -> None:
        await self.set_cash(user_id, self.model.cash + amount)
        return

    async def remove_cash(self, user_id: int, amount: int) -> None:
        await self.set_cash(user_id, self.model.cash - amount)
        return

    async def set_gain(self, user_id: int, amount: Any) -> None:
        await self.edit_one(user_id, {"gain": amount})
        return

    async def add_gain(self, user_id: int, amount: int) -> None:
        await self.set_gain(user_id, self.model.gain + amount)
        return

    async def remove_gain(self, user_id: int, amount: int) -> None:
        await self.set_gain(user_id, self.model.gain - amount)
        return
    
    async def set_wit(self, user_id: int, amount: Any) -> None:
        await self.edit_one(user_id, {"wit": amount})
        return

    async def add_wit(self, user_id: int, amount: int) -> None:
        await self.set_wit(user_id, self.model.wit + amount)
        return
    
    async def remove_wit(self, user_id: int, amount: int) -> None:
        await self.set_wit(user_id, self.model.wit - amount)
        return
