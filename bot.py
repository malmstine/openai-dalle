import json
import os

import logging
import asyncio

from openai import BadRequestError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from telebot.async_telebot import AsyncTeleBot
from domains import answer_bot


logging.basicConfig(filename="fatum.log", format='%(asctime)s %(message)s', filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

USER_WHITE_LIST = [int(user_id) for user_id in os.environ.get("USER_WHITE_LIST").split(":")]
BOT_TOKEN = os.environ.get('BOT_TOKEN')


DB_USER = os.environ.get("DB_USER", "openai-dalle")
DB_PASS = os.environ.get("DB_PASS", "openai-dalle")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_NAME = os.environ.get("DB_NAME", "openai-dalle")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL, echo=True)


def create_session_marker(engine_):
    return sessionmaker(
        engine_, class_=AsyncSession, expire_on_commit=False
    )


async_session = create_session_marker(engine)


try:
    bot = AsyncTeleBot(BOT_TOKEN)


    @bot.message_handler(func=lambda msg: msg.text != "/start")
    async def send_welcome(message):
        if message.from_user.id not in USER_WHITE_LIST:
            return

        await bot.send_chat_action(message.from_user.id, 'typing')
        async with async_session() as session:
            try:
                answer = await answer_bot(session, message.from_user.id, message.text)
            except BadRequestError as ex:
                text = json.loads(ex.response.text)["error"]["message"]
                await bot.send_message(
                    message.chat.id,
                    text
                )
                return
            await bot.send_photo(
                message.chat.id,
                photo=answer
            )
            return answer


    asyncio.run(bot.polling())
except BaseException as ex:
    logger.error(str(ex))
    raise
