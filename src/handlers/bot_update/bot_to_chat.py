from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter, LEFT
from sqlalchemy import select, ScalarResult
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, ContentType, ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.filters.chat_update import AddOrUpdateChatFilter
from src.service.bot_update.chat import add_chat, left_chat, update_to_supergroup
from src.db.models import Auth



router = Router()


@router.message(AddOrUpdateChatFilter())
async def bot_added(message: Message, session: AsyncSession):
    if message.migrate_from_chat_id:
        old_chat_id = message.migrate_from_chat_id
        new_chat_id = message.chat.id
        update = await update_to_supergroup(session, int(old_chat_id), int(new_chat_id))
        if update == False:
            pass

    chat_id = message.chat.id
    chatname = message.chat.full_name
    new_chat = await add_chat(session, chat_id=chat_id, chatname=chatname)
    if new_chat == True:

        await message.answer(text=f"Привет! Спасибо, что добавили меня в группу")



@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> LEFT))
async def bot_deleted(event: ChatMemberUpdated, session: AsyncSession):
    chat_id = event.chat.id
    await left_chat(session, chat_id)

