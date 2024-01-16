import asyncio
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from config import DICE_COMMISSION
from utils.uow import UnitOfWork
from utils.funcs import k_to_int, ranks
from api.middlewares import UOWSessionMiddleware
from api.parser_args import parse_args
from translations import tra 
from utils.models.dice_rooms import DiceRooms


router = Router()
router.message.middleware(UOWSessionMiddleware())

@router.message(Command("h", "help", 'HELP'))
async def rooms(message: Message, uow: UnitOfWork) -> None:
    user = await uow.users.select_one(message.from_user.id)
    Lang = (user.Lang)


    if Lang =='en':
        await message.reply("'/l_ru' - Русский\nLink to the bot's profile in RR - https://rivalregions.com/#slide/profile/2001024035\n\nteam roster:\n/start - Welcome message\n\n/help - Text with list of commands\n\n/account(/acc) {link to your RR account} - Link your RR profile to your Telegram account\n\n/balance(/b) - Shows your balance\n\n/withdraw(/w) {the amount of money you want to withdraw} - Command to withdraw money\n\n/dice(/d) {stake} - A command to create a room for a specified amount\n\n/join(/j) {room number} - Command to enter another person's room\n\n/delete(/del){room number} - Delete your room\n\n/rooms(/r) - View room list\n\nIn order to replenish the balance: First link your RR profile, and then send the bot the amount you want to replenish your balance (If you send money before linking the profile, the money will be lost).\n\nTo access the chat room, click here. (https://t.me/+-Q_LnZ38VGwzZGIy) - ru (https://t.me/+OZ1VeLOxrIE4YzAy) - en.\n\nIf you have any questions - @rim_4965")
    else:
        await message.reply("'/l_en' - English\nСсылка на профиль бота в РР - https://rivalregions.com/#slide/profile/2001024035\n\nсписок команд:\n/start - Приветственное сообщение\n\n/help - Текст со списком команд\n\n/account(/acc) {ссылка на ваш аккаунт в RR} - Привязать свой профиль РР к своему аккаунту в телеграмм\n\n/balance(/bal) - Показывает ваш баланс\n\n/withdraw(/w) {количество денег которое хотите вывести} - Команда для вывода денег\n\n/dice(/d) {ставка} - Команда для создания комнаты на указанную сумму\n\n/join(/j) {номер комнаты} - Команда для захода в чужую комнату\n\n/delete(/del){номер комнаты} - Удалить свою комнату\n\n/rooms(/r) - Посмотреть список комнат\n\nДля того чтобы пополнить баланс: Сначала привяжите свой профиль РР, а потом отправте боту ту сумму на которую хотите пополнить свой баланс(Если вы отправите деньги до привязки профиля то деньги пропадут).\n\nДля того что бы попасть в чат нажмите сюда (https://t.me/+-Q_LnZ38VGwzZGIy) - ru (https://t.me/+OZ1VeLOxrIE4YzAy) - en .\n\nЕжели какие вопросы - @rim_4965")


@router.message(Command("r", "rooms"))
async def rooms(message: Message, uow: UnitOfWork) -> None:
    user = await uow.users.select_one(message.from_user.id)
    Lang = (user.Lang)
    list_rooms = await uow.dice_rooms.select_where_chat_id(message.chat.id)


    text = ''
    num = 0

    for room in list_rooms:
        num += 1
        if Lang=='en':
            text += f"{num}) room {room.id} || {room.owner_name} || {ranks(room.bid)}\n"
        else:        
            text += f"{num}) комната {room.id} || {room.owner_name} || {ranks(room.bid)}\n"

    if not text:
        if Lang=='en':
            text = 'no rooms'
        else:
            text = "Комнат нету("

    await message.reply(text)
    return


@router.message(Command("d", "dice"))
async def dice(message: Message, uow: UnitOfWork) -> None:
    user = await uow.users.select_one(message.from_user.id)
    Lang = (user.Lang)
    #rooms = await uow.dice_rooms.select_where_chat_id(message.chat.id)
    #rooms1 = rooms.user_id

    try:
        bid = parse_args(message, lambda x: "all" if x == "all" else k_to_int(x))[0]
    except (IndexError, ValueError):
        bid = 0

    bal = (await uow.users.select_one(message.from_user.id)).cash

    if bid == "all":
        bid = bal

    if bid < 0:
        if Lang =='en':
            await message.reply("Thief")
        else:
            await message.reply("Воришка")
        return

    if bid > bal:

        await message.reply(tra("Недостаточно денег", Lang))
        return
    
    if await uow.dice_rooms.select_one_where({"owner_id": message.from_user.id, "chat_id": message.chat.id}) is not None:
        await message.reply("нельзя")
        return
    #if user in rooms1:
        #await message.reply(tra("Уже есть комната"))
       # return

    await uow.users.remove_cash(message.from_user.id, bid)
    new_room_id = await uow.dice_rooms.insert(
        message.chat.id, message.from_user.id, message.from_user.first_name, bid)
    if Lang =='en':
        await message.reply(f"Successfully created a room with the id {new_room_id}")
    else:
        await message.reply(f"Успешно создали команту с id {new_room_id}")
    return


@router.message(Command("del", "delete"))
async def delete(message: Message, uow: UnitOfWork) -> None:
    user = await uow.users.select_one(message.from_user.id)
    Lang = (user.Lang)
    try:
        room_id = parse_args(message, int)[0]
    except (IndexError, ValueError):
        if Lang =='en':
            await message.reply("You have to write the id of the room")
        else:
            await message.reply("Надо ввести id комнаты")
        return

    room = await uow.dice_rooms.select_one(room_id)

    if room is None:
        await message.reply(tra("Такой комнаты не существует", Lang))
        #await message.reply("Такой комнаты не существует")
        return

    if message.chat.id != room.chat_id:
        if Lang =='en':
            await message.reply("This room is in another chat room")
        else:
            await message.reply("Данная комната находится в другом чате")
        return

    if message.from_user.id != room.owner_id:
        if Lang =='en':
            await message.reply("You don't own the room")
        else:
            await message.reply("Вы не владелец комнаты")
        return

    await uow.users.add_cash(message.from_user.id, room.bid)
    await uow.dice_rooms.delete_one(room_id)

    await message.reply(tra("Успешно удалили комнату", Lang))
    #await message.reply("Успешно удалили комнату")
    return


@router.message(Command("j", "join"))
async def join(message: Message, uow: UnitOfWork) -> None:
    user = await uow.users.select_one(message.from_user.id)
    Lang = (user.Lang)
    try:
        room_id = parse_args(message, int)[0]
    except (IndexError, ValueError):
        if Lang =='en':
            await message.reply("You have to write the id of the room")
        else:
            await message.reply("Надо ввести id комнаты")
        return

    if not await uow.dice_rooms.exists_by_id_and_chat_id(room_id, message.chat.id):
        if Lang =='en':
            await message.reply("You have to write the id of the room")
        else:        
            await message.reply("This room doesn't exist")
        return


    room = await uow.dice_rooms.select_one(room_id)

    if (await uow.users.select_one(message.from_user.id)).cash < room.bid:
        if Lang =='en':
            await message.reply("Not enough money")
        else:
            await message.reply("Not enough money")
        return

    await uow.dice_rooms.delete_one(room_id)
    await uow.users.remove_cash(message.from_user.id, room.bid)

    owner_data = await message.answer_dice()
    owner_data = int(owner_data.dice.value)

    user_data = await message.answer_dice()
    user_data = int(user_data.dice.value)
    await asyncio.sleep(4)

    gain = int(room.bid / 100 * (100 - DICE_COMMISSION) * 2)
    gainminus = int(room.bid / 100 * 100)

    if owner_data > user_data:
        await uow.users.add_cash(room.owner_id, gain)

        await uow.users.add_gain(room.owner_id, gain)
        await uow.users.remove_gain(message.from_user.id, gainminus)

        if Lang =='en':
            await message.answer(f"Winner {room.owner_name} and earned {ranks(gain)}")
        else:
            await message.answer(f"Победил {room.owner_name} и заработал {ranks(gain)}")

    elif owner_data < user_data:
        await uow.users.add_cash(message.from_user.id, gain)

        await uow.users.add_gain(message.from_user.id, gain)
        await uow.users.remove_gain(room.owner_id, gainminus)
        if Lang =='en':
            await message.answer(f"Winner {message.from_user.first_name} and earned {ranks(gain)}")
        else:
            await message.answer(f"Победил {message.from_user.first_name} и заработал {ranks(gain)}")

    else:
        await uow.users.add_cash(room.owner_id, room.bid)
        await uow.users.add_cash(message.from_user.id, room.bid)
        if Lang =='en':
            await message.answer("It's a tie!")
        else:
            await message.answer("Ничья!")
    return



#@router.message(Command("off"))
#async def bot(message: Message, self, uow: UnitOfWork, profile_id: int) -> None:
   # user = await uow.users.select_by_rr_acc(profile_id)
   # await bot.send_message(user.id,"Бота отключают")
   # return
