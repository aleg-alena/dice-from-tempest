from sqlalchemy import Column, ForeignKey, INTEGER, BIGINT, NCHAR
from utils.db import Base
from utils.models.users import Users


class DiceRooms(Base):
    __tablename__ = "dice_rooms"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    chat_id = Column(BIGINT, nullable=False)
    owner_id = Column(BIGINT, ForeignKey(Users.id), nullable=False)
    owner_name = Column(NCHAR(64), nullable=False)
    bid = Column(BIGINT, nullable=False)
