from aiogram.filters import Command

from helpers.globals import Globals

dp = Globals.dp


@dp.message(Command('start'))
async def start(message):
    await message.answer('Hello! I am a bot')
