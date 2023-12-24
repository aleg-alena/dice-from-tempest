from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command, CommandStart
from config import RR_ACC_ID
from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from utils.uow import UnitOfWork
from utils.funcs import ranks, k_to_int
from api.middlewares import UOWSessionMiddleware
from api.parser_args import parse_args

router = Router()

router.message.middleware(UOWSessionMiddleware())


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.reply("Дарова")
    return

@router.message(Command("l_en", "lang_en", "language_en"))
async def delete(message: Message, uow: UnitOfWork) -> None:
    #Lang = (await uow.users.select_one(message.from_user.id)).Lang
    Lang = 'en'
    #uow.users.set_Lang(message.from_user.id, Lang)
    user = await uow.users.select_one(message.from_user.id)
    #await (f"Ваш язык: {(user.Lang)}")
    await uow.users.set_Lang(message.from_user.id, Lang)
    await message.reply(f"Your language: {(user.Lang)}")
    return

@router.message(Command("l_ru", "lang_ru","language_ru"))
async def delete(message: Message, uow: UnitOfWork) -> None:
    Lang = 'ru'
    #uow.users.set_Lang(message.from_user.id, Lang)
    user = await uow.users.select_one(message.from_user.id)
    #await (f"Ваш язык: {(user.Lang)}")
    await uow.users.set_Lang(message.from_user.id, Lang)
    await message.reply(f"Ваш язык: {(user.Lang)}")
    return



@router.message(Command("don", "donate"))
async def donate(message: Message) -> None:
    await message.reply(f"https://rivalregions.com/#slide/profile/{RR_ACC_ID}")
    return
