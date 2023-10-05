import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from dotenv import load_dotenv

from bot import LanguageBot
from db import DB
from logs import setup_logs


async def main():
    load_dotenv()
    setup_logs(log_level=logging.INFO)

    # Read API token from environment and create bot
    api_token = os.getenv("TG_TOKEN")
    if not api_token:
        raise ValueError("No API token provided")

    # Initialize bot and dispatcher
    bot = Bot(token=api_token)
    dp = Dispatcher()

    db = DB(os.environ)
    logic = LanguageBot(bot, db)

    @dp.message(Command('start'))
    async def start(message):
        await message.answer('Hello! I am a bot')

    await logic.start_in_background()

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
