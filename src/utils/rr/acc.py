import asyncio
import re
import aiohttp
from socket import error as SocketError
from aiogram.exceptions import TelegramForbiddenError
from tgbot import bot
from utils.uow import UnitOfWork
from utils.funcs import ranks
from .parse_rep import parse_html_replenishments


class BotRR:
    async def registration(self) -> None:
        self.session = aiohttp.ClientSession(
            headers = {'User-Agent': self.data_reg['user_agent'],
                       'content-type': 'application/x-www-form-urlencoded'})

        data = {
            'mail': self.data_reg['mail'],
            'p': self.data_reg['password'],
            's': "Отправить"}

        link_auth = 'https://rivalregions.com/rival/pass'

        r = await self.session.post(link_auth, data=data)
        r = await r.text()

        _id = re.search(r'name="id" value="(\d+)"', r).group(1)

        _token = re.search(r'name="access_token" value="(.+)"', r).group(1)

        _hash = re.search(r'name="hash" value="(.+)"', r).group(1)

        await self.session.get(
        f'https://rivalregions.com/?viewer_id={_id}&id={_id}'
        f'&gl_number=&gl_photo=&gl_photo_medium=&gl_photo_big=&tmz_sent'
        f'=3&wdt_sent=1008&access_token={_token}&hash={_hash}')
        return

    def __init__(self, mail: str, password: str, user_agent: str, c_html: str):
        self.data_reg = {"mail": mail, "password": password, "user_agent": user_agent}
        self.c_html = c_html

    async def send_money(self, recipient_id: int, amount: int) -> None:
        data = {'whom': str(recipient_id), 'type': "0", 'n': str(amount), 'c': self.c_html}

        await self.session.post('https://rivalregions.com/storage/donate', data=data)
        return

    async def replenishments_chek(self) -> None:
        r = await self.session.get(f'https://rivalregions.com/log/index/money?c={self.c_html}')
        history_replenishments = parse_html_replenishments(await r.text())

        while True:
            await asyncio.sleep(10)

            try:
                r = await self.session.get(f'https://rivalregions.com/log/index/money?c={self.c_html}')
                page = await r.text()
            except SocketError:
                continue

            replenishments = parse_html_replenishments(page)

            if replenishments == history_replenishments:
                continue

            async with UnitOfWork() as uow:
                for rep in replenishments:
                    if rep in history_replenishments:
                        continue

                    await self.handle_rep(uow, rep['profile_id'], rep['amount'])
                    continue

            history_replenishments = replenishments
            continue

    async def handle_rep(self, uow: UnitOfWork, profile_id: int, amount: int) -> None:
        user = await uow.users.select_by_rr_acc(profile_id)

        if user is None:
            return

        await uow.users.add_cash(user.id, amount)

        try:
            await bot.send_message(user.id, f"Успешно пополнили {ranks(amount)}")
        except TelegramForbiddenError:
            pass
        return
