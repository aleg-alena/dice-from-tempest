import asyncio
import api
from utils.rr import rr_bot
from tgbot import bot, dp

api.register_routers(dp)


async def main() -> None:
    print("Начинаю работать...")
    await rr_bot.registration()
    asyncio.create_task(rr_bot.replenishments_chek())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)







if __name__ == "__main__":
    asyncio.run(main())
