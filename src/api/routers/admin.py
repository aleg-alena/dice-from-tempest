from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from utils.uow import UnitOfWork
from utils.funcs import k_to_int
from api.middlewares import UOWSessionMiddleware
from api.filters import IsOwner
from api.parser_args import parse_args

router = Router()
router.message.middleware(UOWSessionMiddleware())
router.message.filter(IsOwner())


@router.message(Command("hack"))
async def hack(message: Message, uow: UnitOfWork) -> None:
    if message.reply_to_message is None:
        target_id = message.from_user.id
    else:
        target_id = message.reply_to_message.from_user.id

    try:
        hack_type, amount = parse_args(message, str.upper, k_to_int)
    except IndexError:
        await message.reply("Надо ввести типо взлома и количество взлома")
        return
    except ValueError:
        await message.reply("Количество взлома должно быть числом")
        return

    await uow.users.insert_or_ignore(target_id)

    match hack_type:
        case "SET":
            await uow.users.set_cash(target_id, amount)
            await message.reply("Успешно установили количество денег")
        case "ADD":
            await uow.users.add_cash(target_id, amount)
            await message.reply("Успешно добавили количество денег")
        case "REMOVE":
            await uow.users.remove_cash(target_id, amount)
            await message.reply("Успешно отняли количество денег")
        case "WIT":
            await uow.users.remove_wit(target_id, amount)
            await message.reply("Банк вывода был анулирован")
        case _:
            await message.reply("Непонятный типо взлома")
    return
