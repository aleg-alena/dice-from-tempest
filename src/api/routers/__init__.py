from aiogram import Dispatcher
from . import other
from . import money
from . import account
from . import admin
from . import dice
from . import donation_rr

routers = [
    other.router,
    money.router,
    account.router,
    admin.router,
    dice.router,
    donation_rr.router
]


def register_routers(dp: Dispatcher) -> None:
    dp.include_routers(*routers)
