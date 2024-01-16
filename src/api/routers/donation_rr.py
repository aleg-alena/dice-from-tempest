from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from utils.uow import UnitOfWork
from utils.funcs import k_to_int
from utils.rr import rr_bot
from api.middlewares import UOWSessionMiddleware
from api.parser_args import parse_args
from translations import tra 

router = Router()
router.message.middleware(UOWSessionMiddleware())


@router.message(Command("w", "withdraw"))
async def withdraw(message: Message, uow: UnitOfWork) -> None:
    user = await uow.users.select_one(message.from_user.id)
    Lang = (user.Lang)
    try:
        amount = parse_args(message, lambda x: "all" if x == "all" else k_to_int(x))[0]
    except (IndexError, ValueError):
        if Lang =='en':
            await message.reply("You have to enter the amount of output")
        else:
            await message.reply("Надо ввести количество вывода")
        return

    user = await uow.users.select_one(message.from_user.id)

    if amount == 'all':
        amount = user.cash

    if amount < 0:
        if Lang =='en':
            await message.reply("Don't, Uncle.")
        else:
            await message.reply("Ненадо дядя")
        return

    if user.rr_acc is None:
        if Lang =='en':
            await message.reply("You haven't linked your account")
        else:
            await message.reply("Вы не привязали аккаунт")
        return

    if amount > user.cash:
        if Lang =='en':
            await message.reply("Not enough money")
        else:
            await message.reply("Недостаточно денег")
        return
    amount1=amount-(amount/100*3)
    await uow.users.remove_cash(message.from_user.id, amount)
    await uow.users.add_wit(message.from_user.id, amount1)
    if Lang =='en':
        await message.reply("The conclusion is written down!")
    else:
        await message.reply("Вывод записан!")
    return
