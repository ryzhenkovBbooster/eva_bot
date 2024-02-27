import json

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import sessionmaker
from src.db.models import Auth
from src.filters.guard import UserAccessFilter
from src.keyboards.for_admin import get_all, edit_access_k, crud_premission, users_key
from src.service.admin.access import Add_access, users_service, edit_access_service
from src.structure.misc import redis
from src.service.admin.chats import get_active_unactiv_groups_service
from src.keyboards.for_admin import get_chats, cancel_key, get_all_from_chat_key
from src.FSM.update_curator import CuratorUpdate

log = []

router = Router()

@router.callback_query(Add_access.get_user, F.data == 'cancel')
@router.callback_query(Add_access.edit_access, F.data == 'cancel')
async def back_to_menu_inline(callback: CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.answer('back to menu', reply_markup=crud_premission())
## хендлер который возвращает пользователей о которых знает бот

@router.message(F.text.lower() == "users", UserAccessFilter(session_pool=sessionmaker))
async def answer_users_bot(message: Message, session: AsyncSession):
        result = await session.execute(select(Auth))
        result: ScalarResult
        users: Auth = result.all()
        users_str = "\n".join(map(str, (user[0] for user in users)))
        while 'True' in users_str or 'False' in users_str:
                users_str = users_str.replace('True', 'admin').replace('False', 'client')


        await message.answer(users_str, reply_markup=users_key())




## хедлер, который возвращает назад, в главное меню
@router.callback_query(Add_access.get_user, F.data =='back_to_menu')
@router.callback_query(Add_access.edit_access, F.data =='back_to_menu')
async def back_to_admin_menu(callback: CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.answer('back to menu', reply_markup=crud_premission())

## хендлер который переводит бота в fsm для выдачи доступа юзеру, состоняие в котором нужно выбрать пользователя
@router.message(F.text.lower() == "access", UserAccessFilter(session_pool=sessionmaker))
async def access(message: Message, state: FSMContext, session: AsyncSession):
        arr = await users_service(session)

        await message.answer(
                'Выберите пользователя', reply_markup= await get_all(arr)
        )
        await state.set_state(Add_access.get_user)

## хендлер который переводит бота в fsm для выдачи доступа юзеру, состоняние в котором мы видим уровень доступа у пользователя и можем его изменить
@router.callback_query(Add_access.get_user)
async def add_delete_admin(callback: CallbackQuery, state: FSMContext, session: AsyncSession ):
        redis_key = callback.data
        user_json = await redis.get(redis_key)
        user = json.loads(user_json)
        # info = await about_user_service(session=session, username=callback.data)
        await state.update_data(about_user=user['access'], user_id=user['user_id'],username=user['username'] )


        await callback.message.answer(f"Пользователь {user['username']} - {user['access']}",
                                      reply_markup=edit_access_k())


        await state.set_state(Add_access.edit_access)

##хендлер который переводит бота в fsm для выдачи доступа юзеру, состояние в котором меняется уровень доступа

@router.callback_query(Add_access.edit_access)
async def new_access(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
        user = await state.get_data()

        await edit_access_service(
                session=session,
                user=user['username'],
                user_info=user['about_user'],
                user_id=user['user_id'])

        await callback.message.answer('Доступ изменен')
        await state.clear()

## возвращает в главное меню
@router.message(F.text.lower() == "главное меню", UserAccessFilter(session_pool=sessionmaker))
async def back_to_menu(message: Message):
        await message.answer('back to menu',reply_markup=crud_premission())






@router.message(F.text.lower() == 'clear cache', UserAccessFilter(session_pool=sessionmaker))
async def clear_cache(message: Message):
        await redis.flushall()
        await message.answer('cache cleared')

