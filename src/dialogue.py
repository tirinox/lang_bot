import logging

from aiogram import Dispatcher
from aiogram.types import Message

from manager import Manager, Session
from tts import generate_date_text_ja, random_date, tts

QUERY_TEST = '何月何日ですか？'

logger = logging.getLogger(__name__)


def register_dialogs(dp: Dispatcher, mananger: Manager):
    async def tick_handler(session: Session):
        await dp.bot.send_message(session.student_ident, 'Tick!')
        return session

    mananger.handler = tick_handler

    async def ask_date(message: Message):
        dt = random_date()
        text = generate_date_text_ja(dt)
        audio_file = tts(text)
        audio_file.name = f'{QUERY_TEST}.mp3'
        logger.info(f'Sending audio file to user {message.from_user.id}, cation: "{text}"')
        await message.answer_audio(audio_file, caption=QUERY_TEST)

    @dp.message_handler(commands=['start', 'help'])
    async def send_welcome(message: Message):
        await message.reply("Lang bot 0.1: Japanese dates TTS")

    @dp.message_handler(commands=['register'])
    async def register(message: Message):
        logging.info(f"New incoming register message from user {message.from_user.id}")
        mananger.register_student(message.from_user.id, 60)
        await message.answer('You are registered!')

    @dp.message_handler(commands=['unregister'])
    async def unregister(message: Message):
        logging.info(f"New incoming unregister message from user {message.from_user.id}")
        mananger.unregister_student(message.from_user.id)
        await message.answer('You are unregistered!')

    @dp.message_handler()
    async def echo(message: Message):
        await message.answer('Unknown command.')
