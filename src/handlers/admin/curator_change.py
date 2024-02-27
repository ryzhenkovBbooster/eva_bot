import json

from aiogram import F, Router

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.FSM.update_curator import CuratorUpdate
from src.db.database import sessionmaker
from src.filters.guard import UserAccessFilter
from src.handlers.admin.chat import get_one_active_chat
from src.keyboards.for_admin import crud_premission, get_all_from_chat_key
from src.service.admin.access import users_service
from src.service.admin.chats import get_active_unactiv_groups_service
from src.keyboards.change_curator_k import get_all_items_from_change_curator_k
from src.service.admin.curator_change_service import update_curator_service, get_chats_from_change_curator, \
    get_old_curator_id
from src.structure.misc import redis

router = Router()

@router.callback_query(CuratorUpdate.get_chats, F.data == 'back_to_menu')
@router.callback_query(F.data == 'back_to_menu')
async def back_to_menu(callback: CallbackQuery):
    await callback.message.answer('back to menu', reply_markup=crud_premission())








# async def get_chats_handle(message: Message, session: AsyncSession, state: FSMContext):
#         chats = await get_chats_from_change_curator(session)
#         if chats:
#                 await state.set_state(CuratorUpdate.get_chats)
#                 await message.answer(text='в каком чате хотите поменять куратора?',
#                                      reply_markup=get_all_items_from_change_curator_k(chats,key='chatname',id='chat_id' ))
#         else:
#                 await message.answer(text='err: активные чаты не найдены')


@router.message(F.text.lower() == "change curator", UserAccessFilter(session_pool=sessionmaker))
async def get_curators(message: Message, session: AsyncSession, state: FSMContext):

    curators = await users_service(session)
    for cur in curators:
        if cur['access'] == 'client':
            curators.remove(cur)

    await state.set_state(CuratorUpdate.get_curators)
    await message.answer(text='Наши потенциальные кураторы', reply_markup=get_all_items_from_change_curator_k(curators, key='username', id='user_id'))


@router.callback_query(CuratorUpdate.get_curators)
async def change_curator(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    curator = callback.data
    chat_id = data['chat_id']
    old_curator = await get_old_curator_id(session, chat_id)
    edior = callback.from_user.username



    put_curator_inChat = await update_curator_service(session, int(curator), int(chat_id))
    if put_curator_inChat:
        link = await callback.bot.export_chat_invite_link(chat_id=chat_id)
        cache = await redis.delete(str(chat_id))
        print(cache)
        await callback.message.answer('Куратор изменен')
        await callback.bot.send_message(curator, text=f'Вы стали куратором в чате: {link}')
        await callback.bot.send_message(old_curator, text=(f'Вы больше не куратор в чате: {link}\n'
                                                      f'Человек внесший изменения: @{edior}'))

        await state.update_data(curator_changed=True)
        await get_one_active_chat(callback, state, session)

    else:
        await callback.message.answer('err: ошибка при обновлении данных в бд')

