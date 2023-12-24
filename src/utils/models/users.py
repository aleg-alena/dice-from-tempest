from sqlalchemy import Column, BIGINT
from utils.db import Base
from enum import Enum, auto


class Users(Base):
    __tablename__ = "users"

    id = Column(BIGINT, primary_key=True, autoincrement=False)
    rr_acc = Column(BIGINT)
    cash = Column(BIGINT, default=0, nullable=False)
    gain = Column(BIGINT, default=0, nullable=False)
    Lang = Column(BIGINT, default='ru', nullable=False)
    #class Lang(int, Enum):
        #ru = auto()
        #en = auto()





