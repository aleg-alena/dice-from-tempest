from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from utils.uow import UnitOfWork
from api.middlewares import UOWSessionMiddleware
from translations import tra

router = Router()
router.message.middleware(UOWSessionMiddleware())


@router.message(Command("acc", "account"))
async def acc(message: Message, uow: UnitOfWork) -> None:
    user = await uow.users.select_one(message.from_user.id)
    Lang = (user.Lang)
    args = message.text.split()[1:]

    if len(args) == 0:
        acc_id = (await uow.users.select_one(message.from_user.id)).rr_acc

        if acc_id is None:
            if Lang =='en':
                await message.reply("You haven't linked your account")
            else:
                await message.reply("Вы не привязали аккаунт")
            return
        if Lang =='en':
            await message.reply(f"Your accaunt: https://rivalregions.com/#slide/profile/{acc_id}")
        else:    
            await message.reply(f"Ваш аккаунт: https://rivalregions.com/#slide/profile/{acc_id}")
        return
    elif len(args) > 1:
        if Lang =='en':
            await message.reply("You have to enter the account link")
        else:
            await message.reply("Надо ввести ссылку на аккаунт")
        return

    try:
        acc_id = int(args[0]
                    .replace('m.', '')
                    .replace('https://rivalregions.com/#slide/profile/', ''))
    except ValueError:
        if Lang =='en':
            await message.reply("The account link is wrong")
        else:
            await message.reply("Ссылка на аккаунт неправильная")
        return

    acc_owner = await uow.users.select_by_rr_acc(acc_id)
    if acc_owner is not None:
        if Lang =='en':
            await message.reply("This account is already taken")
        else:
            await message.reply("Данный аккаунт уже занят")
        return

    await uow.users.set_rr_acc(message.from_user.id, acc_id)
    if Lang =='en':
        await message.reply("Successfully installed the account link")
    else:
        await message.reply("Успешно установили ссылку на аккаунт")
    return
