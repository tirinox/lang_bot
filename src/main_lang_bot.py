import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from dotenv import load_dotenv

from logic.bot import LanguageBot
from helpers.db import DB
from helpers.logs import setup_logs
from helpers.globals import Globals


async def main():
    load_dotenv()
    setup_logs(log_level=logging.INFO)

    # Read API token from environment and create bot
    api_token = os.getenv("TG_TOKEN")
    if not api_token:
        raise ValueError("No API token provided")

    # Initialize bot and dispatcher
    bot = Bot(token=api_token)

    Globals.db = DB(os.environ)
    Globals.logic = LanguageBot(bot, Globals.db)

    await Globals.logic.start_in_background()

    await Globals.dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
