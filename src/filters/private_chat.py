from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from aiogram.types import TelegramObject
from sqlalchemy import select, ScalarResult
from src.db.models import Auth
class PrivateChat(BaseFilter):



    async def __call__(self, message: Message):

        if message.chat.type != ChatType.PRIVATE:
            return False
        else:
            return True
