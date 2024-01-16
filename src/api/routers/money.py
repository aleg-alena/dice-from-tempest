from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from utils.uow import UnitOfWork
from utils.funcs import ranks, k_to_int
from api.middlewares import UOWSessionMiddleware
from api.parser_args import parse_args
from translations import tra 

router = Router()
router.message.middleware(UOWSessionMiddleware())


@router.message(Command("b", "bal", "balance"))
async def balance(message: Message, uow: UnitOfWork) -> None:
    user = await uow.users.select_one(message.from_user.id)
    Lang = (user.Lang)
    user = await uow.users.select_one(message.from_user.id)
    if Lang == 'en':
        await message.reply(f"Your Balance: {ranks(user.cash)}\ntotal wins: {ranks(user.gain)}\nWithdrawal bank: {ranks(user.wit)}")
    else:
        await message.reply(f"Ваш баланс: {ranks(user.cash)}\nВсего выиграно: {ranks(user.gain)}\nБанк вывода: {ranks(user.wit)}")
    return


@router.message(Command("g", "give"))
async def give(message: Message, uow: UnitOfWork) -> None:
    user = await uow.users.select_one(message.from_user.id)
    Lang = (user.Lang)
    if message.reply_to_message is None:

        if Lang == 'en':
            await message.reply("Replay the user you want to give the money to")
        else:
            await message.reply("Сделайте реплай на юзера которому хотите передать деньги")
        return

    target_id = message.reply_to_message.from_user.id

    try:
        amount = parse_args(message, lambda x: "all" if x == "all" else k_to_int(x))[0]
    except IndexError:
        if Lang == 'en':
            await message.reply("Enter the amount of money you want to transfer")
        else:
            await message.reply("Введите количество денег которое хотите передать")
        return
    except ValueError:
        if Lang == 'en':
            await message.reply("The amount of money has to be a number")
        else:
            await message.reply("Количество денег должно быть числом")
        return

    await uow.users.insert_or_ignore(target_id)

    bal = (await uow.users.select_one(message.from_user.id)).cash

    if amount == 'all':
        amount = bal

    if amount < 0:
        if Lang == 'en':
            await message.reply("Thief ayayai")
        else:
            await message.reply("Воришка аяяй")
        return

    if amount > bal:
        if Lang == 'en':
            await message.reply("Not enough money")
        else:
            await message.reply("Недостаточно денег")
        return

    await uow.users.remove_cash(message.from_user.id, amount)
    await uow.users.add_cash(target_id, amount)
    if Lang == 'en':
        await message.reply(f"Successfully transferred {ranks(amount)}")
    else:
        await message.reply(f"Успешно перевели {ranks(amount)}")
    return
