from aiogram import Dispatcher

from helpers.db import DB
from logic.bot import LanguageBot


class Globals:
    dp = Dispatcher()
    logic: LanguageBot = None
    db: DB = None
