import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from dotenv import load_dotenv
from src.middlewares.db import DbSessionMiddleware
from src.middlewares.register_check import RegisterCheck
from src.db.database import sessionmaker
from src.handlers.admin import main_list, access, chat, curator_change
from src.handlers.client import client, prob_period
from src.handlers.bot_update import bot_to_chat
from src.service.admin.course_june import scheduler
from src.structure.misc import redis

logging.basicConfig(level=logging.INFO)
load_dotenv()
# https://progr.interplanety.org/en/removing-the-passing-coroutines-is-forbidden-use-tasks-explicitly-error-when-using-aioschedule-in-python-3-11/
# url for fix tusk aio ERROR
###!bG2$B5DipTV3%bd

bot = Bot(token=os.getenv("TOKEN"))

dp = Dispatcher(storage=RedisStorage(redis=redis))

async def on_startup():
    asyncio.create_task(scheduler(bot, sessionmaker, os.getenv("TIMES")))

## функция в которой зарегестрированы все роутеры колбаки и мидлвейры
async def main():
    dp.startup.register(on_startup)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    dp.message.middleware(RegisterCheck(session_pool=sessionmaker))

    dp.callback_query.middleware(RegisterCheck(session_pool=sessionmaker))

    dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.include_routers(main_list.router,access.router, bot_to_chat.router, chat.router, client.router, curator_change.router, prob_period.router)


    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)





if __name__ == "__main__":
    asyncio.run(main())
