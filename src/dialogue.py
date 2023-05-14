import logging
import random

from aiogram import Dispatcher, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from manager import Manager, Session
from tts import generate_date_text_ja, random_date, tts

QUERY_TEST = '何月何日ですか？'

logger = logging.getLogger(__name__)


def register_dialogs(dp: Dispatcher, mananger: Manager):
    async def tick_handler(session: Session):
        # await dp.bot.send_message(session.student_ident, 'Tick!')
        try:
            session.last_question = await ask_date(dp.bot, session.student_ident)
        except Exception as e:
            logger.exception(e)
            return
        return session

    mananger.handler = tick_handler

    async def ask_date(bot: Bot, user_id):
        dt = random_date()
        text = generate_date_text_ja(dt)
        audio_file = tts(text)
        audio_file.name = f'{QUERY_TEST}.mp3'
        logger.info(f'Sending audio file to user {user_id}, cation: "{text}"')

        answers = [text]
        while len(answers) < 4:
            bad_date = random_date()
            if bad_date not in answers:
                answers.append(generate_date_text_ja(bad_date))
        random.shuffle(answers)
        buttons = [
            [KeyboardButton(answers[0]), KeyboardButton(answers[1])],
            [KeyboardButton(answers[2]), KeyboardButton(answers[3])],
            [KeyboardButton('/unregister')]
        ]

        await bot.send_audio(user_id, audio_file, caption=QUERY_TEST, reply_markup=ReplyKeyboardMarkup(buttons))
        return text

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
        session = mananger.sessions.get(message.from_user.id)
        if session is None:
            await message.answer('You are not registered!\nFirst, register with /register')
            return

        if message.text == session.last_question:
            await message.answer('Correct!', reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer('Wrong!', reply_markup=ReplyKeyboardRemove())
