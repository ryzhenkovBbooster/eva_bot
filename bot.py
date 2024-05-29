import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from cron_job.send_message_from_chat_june import MessageScheduler
from src.middlewares.db import DbSessionMiddleware
from src.middlewares.register_check import RegisterCheck
from src.db.database import sessionmaker
from src.handlers.admin import main_list, access, chat, curator_change
from src.handlers.client import client, prob_period
from src.handlers.bot_update import bot_to_chat
from src.service.admin.course_june import scheduler
from src.static.chat_june import texts
from src.structure.misc import redis

logging.basicConfig(level=logging.INFO)
load_dotenv()
# https://progr.interplanety.org/en/removing-the-passing-coroutines-is-forbidden-use-tasks-explicitly-error-when-using-aioschedule-in-python-3-11/
# url for fix tusk aio ERROR
###v.malovanova@bbooster.ioв
curr_file = os.path.dirname(os.path.realpath(__file__))
images = os.path.join(curr_file, 'src' ,'static', 'picture_to_chat_june')
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(storage=RedisStorage(redis=redis))

async def on_startup():
    scheduler_instance = MessageScheduler(bot=bot, texts=texts, images_dir=images, chat_id=int(os.getenv("JUNE_CHAT")))

    asyncio.create_task(scheduler(bot, sessionmaker, os.getenv("TIMES")))

    asyncio.create_task(schedule_messages(scheduler_instance))


async def schedule_messages(scheduler_instance):
    scheduler = AsyncIOScheduler()

    # Schedule messages from Monday to Friday at 9:30 and 14:30
    scheduler.add_job(scheduler_instance.send_message_with_image, 'cron', day_of_week='mon-fri',  hour=9, minute=30)
    scheduler.add_job(scheduler_instance.send_message_with_image, 'cron', day_of_week='mon-fri',  hour=14, minute=30)

    scheduler.start()
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


# print(images)


if __name__ == "__main__":

    asyncio.run(main())
