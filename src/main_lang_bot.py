import logging
import os

from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv

from dialogue import register_dialogs
from manager import Manager


def main():
    load_dotenv()

    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Read API token from environment and create bot
    api_token = os.getenv("TG_TOKEN")
    if not api_token:
        raise ValueError("No API token provided")

    proxy = os.getenv("TG_PROXY") or None

    # Initialize bot and dispatcher
    bot = Bot(token=api_token, proxy=proxy)
    dp = Dispatcher(bot)

    manager = Manager('sessions.json')
    register_dialogs(dp, manager)

    # Start the Bot
    executor.start_polling(dp, skip_updates=True, on_startup=manager.run_in_background)


if __name__ == '__main__':
    main()
