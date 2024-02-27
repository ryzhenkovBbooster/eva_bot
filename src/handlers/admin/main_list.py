from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from src.db.database import sessionmaker
from src.filters.guard import UserAccessFilter
from src.filters.private_chat import PrivateChat
from src.keyboards.for_admin import crud_premission
from src.keyboards.for_mainl_list import auth

log = []

router = Router()

@router.message(Command('start', prefix='!/') )
async def cmd_start(message: Message):
    if message.chat.type == 'private':

        await message.answer(
            "hello, world!",
            reply_markup=auth()
        )
    else:
        await message.answer(f'hello man {message.from_user.full_name}')


@router.message(F.text.lower() == 'auth', UserAccessFilter(session_pool=sessionmaker), PrivateChat())
async def register(message: Message):
    await message.answer(f'Hello admin {message.from_user.full_name}', reply_markup=crud_premission())









