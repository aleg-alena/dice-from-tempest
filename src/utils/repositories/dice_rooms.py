from utils.abstract_repository import AbstractRepository
from utils.models.dice_rooms import DiceRooms


class DiceRoomsRepository(AbstractRepository):
    model = DiceRooms

    async def select_where_chat_id(self, chat_id: int) -> list[DiceRooms]:
        return await self.select_many({"chat_id": chat_id})

    async def insert(self, chat_id: int, owner_id: int, owner_name: str, bid: int) -> int:
        return await self.insert_one_data({
            "chat_id": chat_id, "owner_id": owner_id, "owner_name": owner_name, "bid": bid})

    async def exists_by_id_and_chat_id(self, room_id: int, chat_id: int) -> bool:
        return await self.exists_where({"id": room_id, "chat_id": chat_id})
