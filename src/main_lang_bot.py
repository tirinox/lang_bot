import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from tts import generate_date_text_ja, tts, random_date

load_dotenv()

API_TOKEN = os.getenv("TG_TOKEN")
if not API_TOKEN:
    raise ValueError("No API token provided")

PROXY = os.getenv("TG_PROXY") or None

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, proxy=PROXY)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Lang bot 0.1: Japanese dates TTS")


@dp.message_handler(commands=['date'])
async def send_date(message: types.Message):
    logging.info(f"New incoming message from user {message.from_user.id}")
    dt = random_date()
    text = generate_date_text_ja(dt)
    audio_file = tts(text)
    audio_file.name = f'out-{text}.mp3'
    logging.info(f'Sending audio file to user {message.from_user.id}, cation: "{text}"')
    await message.answer_audio(audio_file, caption=text)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
