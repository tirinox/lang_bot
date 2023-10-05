from aiogram import Bot

from db import DB


class LanguageBot:
    def __init__(self, tg_bot: Bot, db: DB):
        self.tg_bot = tg_bot
        self.db = db

    async def start_in_background(self):
        ...
