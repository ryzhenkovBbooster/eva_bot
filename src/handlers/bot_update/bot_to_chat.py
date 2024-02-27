from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter, LEFT
from sqlalchemy import select, ScalarResult
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, ContentType, ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.service.bot_update.chat import add_chat,left_chat
from src.db.models import Auth



router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> IS_MEMBER))
async def bot_added(event: ChatMemberUpdated, session: AsyncSession):
    chat_id = event.chat.id
    chatname = event.chat.full_name
    new_chat = await add_chat(session, chat_id=chat_id, chatname=chatname)
    if new_chat == True:

        await event.answer(text=f"Привет! Спасибо, что добавили меня в группу")
    else:
        await event.answer('В моей памяти есть данные что был здесь ранее, и теперь я здесь снова!')


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> LEFT))
async def bot_deleted(event: ChatMemberUpdated, session: AsyncSession):
    chat_id = event.chat.id
    await left_chat(session, chat_id)

