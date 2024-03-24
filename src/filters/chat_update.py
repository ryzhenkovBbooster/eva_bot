from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from aiogram.types import TelegramObject
from sqlalchemy import select, ScalarResult
from src.db.models import Auth
class AddOrUpdateChatFilter(BaseFilter):



    async def __call__(self, message: Message):
        if message.migrate_from_chat_id:
            return True
        if message.new_chat_members:
            for user in message.new_chat_members:
                user_id = user.id
                if user_id == message.bot.id:
                    return True
        else:
            return False
