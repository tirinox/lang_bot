from aiogram import Bot

from helpers.db import DB
from heartbeat import Heartbeat
from helpers.logs import WithLogger


class LanguageBot(WithLogger):
    def __init__(self, tg_bot: Bot, db: DB):
        super().__init__()
        self.tg_bot = tg_bot
        self.db = db
        self.heartbeat = Heartbeat(db, interval=5)

    async def start_in_background(self):
        self.heartbeat.run_in_background()
