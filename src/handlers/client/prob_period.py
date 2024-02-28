import json

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.handlers.client.client import finaly_stage
from src.keyboards.for_admin import message_from_create_photo_key, finaly_message_from_junior_key, \
    message_from_all_invates_key
from src.service.admin.chats import check_user_in_chat
from src.service.admin.course_june import finaly_stage_service, add_column_service, info_about_chat
from src.static.course_june.text import completed_skillup, send_info_about_photo, send_table_from_manager, drop_ipo, \
    invate_to_meeting_is, invate_to_learn_users, finaly_is_from_chat_with_user, finaly_is_from_chat_is
from src.structure.misc import redis

router = Router()
# data 'email': june_data['create_email'],
#             'user_id': chat_data['user_chat_id'],
#             'manager': june_data['manager'],
#             'curator': june_data['curator'],
#             'practical_tasks': june_data['create_practical_task'],
#             'chat_id': chat_data['chat_id'],
#             'personal_folder': june_data['personal_folder_link'],
#             'name': june_data['name_june'],
#             'manager_username': auth_data['username'],
#             'rang': june_data['rang'],
#             'username': chat_data['username'],

@router.message(F.text.lower() == 'текста для ис')
async def all_message_from_this_period(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer('Все шаблоны', reply_markup=finaly_message_from_junior_key())



@router.message(F.text.lower() == 'skill-up правильный')
async def tasks_in_skillup_is_compeleted(message: Message, session: AsyncSession, state: FSMContext):
    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']
    # data кешурестся в redis name = chat_id + user_id
    data = await info_about_chat(session, int(chat_id), int(message.from_user.id))
    if data:


        table = data['evo_table']
        #
        june = data['user_id']
        june_username = await message.bot.get_chat(int(june))
        june_username = june_username.username
        #
        june_chat_id = '-1001445639120'
        is_chat_id = '-1001248647604'
        chatname = data['chatname']
        #
        manager = data['manager']
        manager_username = await message.bot.get_chat(int(manager))
        manager_username = manager_username.username
        #
        chatname = chatname.replace('ТН', 'ИС')

        link_from_is_chat = await message.bot.export_chat_invite_link(int(is_chat_id))

        if await check_user_in_chat(june, june_chat_id, message):
            await message.bot.ban_chat_member(chat_id=june_chat_id, user_id=june)

        await message.bot.set_chat_title(chat_id=chat_id, title=chatname)
        await message.bot.send_message(chat_id=chat_id, text=completed_skillup(june_username, manager_username))
        # await message.bot.send_message(chat_id=chat_id, text=f"Теперь ты на испытательном сроке, вступи в этот [чат]({link_from_is_chat})", parse_mode='Markdown')
        await message.bot.send_message(chat_id=manager, text=send_table_from_manager(june_username, link=table), parse_mode='Markdown')
        await message.answer('Метод выполнен')
    else:
        await message.answer('ты не куратор в этом чате, поэтому ты не можешь отправить сообщение')



@router.message(F.text.lower() == 'фото, подпись')
async def photo_from_junior(message: Message, session: AsyncSession):
    await message.answer(text='выбырите что именно вам нужно', reply_markup=message_from_create_photo_key())

@router.message(F.text.lower() == 'приглашения')
async def all_invates(message: Message):
    await message.answer(text='выбырите что именно вам нужно',reply_markup=message_from_all_invates_key())

@router.message(F.text.lower() == 'фото для подписи')
async def drop_photo(message: Message, state: FSMContext, session: AsyncSession):
    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']
    # data кешурестся в redis name = chat_id + user_id
    data = await info_about_chat(session,int(chat_id), int(message.from_user.id))
    if data:


        june = data['user_id']
        june_username = await message.bot.get_chat(int(june))
        june_username = june_username.username

        link_chat = await message.bot.export_chat_invite_link(chat_id)
        text = send_info_about_photo(june_username)
        await message.bot.send_message(chat_id=chat_id,text=f"{text['first']}")
    else:
        await message.answer('ты не куратор в этом чате, поэтому ты не можешь отправить сообщение')

@router.message(F.text.lower() == 'инструкция про подпись')
async def instruction_about_photo(message: Message, state: FSMContext, session: AsyncSession):
    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']
    # data кешурестся в redis name = chat_id + user_id
    data = await info_about_chat(session, int(chat_id), int(message.from_user.id))
    if data:
        june = data['user_id']
        june_username = await message.bot.get_chat(int(june))
        june_username = june_username.username

        link_chat = await message.bot.export_chat_invite_link(chat_id)
        text = send_info_about_photo(june_username)
        await message.bot.send_message(chat_id=chat_id,text=f"{text['second']}", parse_mode='Markdown')
    else:
        await message.answer('ты не куратор в этом чате, поэтому ты не можешь отправить сообщение')

@router.message(F.text.lower() == 'фото + девиз')
async def drop_photo_from_meeting(message: Message, state: FSMContext, session: AsyncSession):
    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']
    # data кешурестся в redis name = chat_id + user_id
    data = await info_about_chat(session, int(chat_id), int(message.from_user.id))
    if data:
        june = data['user_id']
        june_username = await message.bot.get_chat(int(june))
        june_username = june_username.username


        link_chat = await message.bot.export_chat_invite_link(chat_id)
        text = send_info_about_photo(june_username)
        await message.bot.send_message(chat_id=chat_id, text=f"{text['third']}")
    else:
        await message.answer('ты не куратор в этом чате, поэтому ты не можешь отправить сообщение')


@router.message(F.text.lower() == 'приглашение на встречи ис')
async def invate_to_learning_group_meeting(message: Message, state: FSMContext, session: AsyncSession):
    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']
    # data кешурестся в redis name = chat_id + user_id
    data = await info_about_chat(session, int(chat_id), int(message.from_user.id))
    if data:
        june = data['user_id']
        june_username = await message.bot.get_chat(int(june))
        june_username = june_username.username


        await message.bot.send_message(chat_id=chat_id, text=f'{invate_to_meeting_is(june_username)}')
    else:
        await message.answer('ты не куратор в этом чате, поэтому ты не можешь отправить сообщение')


@router.message(F.text.lower() == 'close')
async def close_chat_with_junior(message: Message, session: AsyncSession, state: FSMContext):
    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']
    # data кешурестся в redis name = chat_id + user_id
    data = await info_about_chat(session, int(chat_id), int(message.from_user.id))
    if data:
        june = data['user_id']
        june_username = await message.bot.get_chat(int(june))
        june_username = june_username.username

        is_chat_id = '-1001248647604'


        # link_chat = await message.bot.export_chat_invite_link(chat_id)
        await message.bot.send_message(chat_id=chat_id,text=f'{finaly_is_from_chat_with_user(june_username)}')
        await message.bot.send_message(chat_id=is_chat_id ,text=f'{finaly_is_from_chat_is(june_username)}')
        close_active_chat = await finaly_stage_service(session, chat_id)
        await add_column_service(message, session, 'finaly_stage', 'true')

        if close_active_chat:

            await message.answer(text='чат закрыт')
    else:
        await message.answer('ты не куратор в этом чате, поэтому ты не можешь отправить сообщение')

@router.message(F.text.lower() == 'выдача ипо сотруднику')
async def invate_to_ipo_course(message: Message, state: FSMContext, session: AsyncSession):
    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']
    # data кешурестся в redis name = chat_id + user_id
    data = await info_about_chat(session, int(chat_id), int(message.from_user.id))
    if data:
        june = data['user_id']
        june_username = await message.bot.get_chat(int(june))
        june_username = june_username.username

        manager = data['manager']
        manager_username = await message.bot.get_chat(int(manager))
        manager_username = manager_username.username

        sheet_ipo = data['practical_tasks']


        link_chat = await message.bot.export_chat_invite_link(chat_id)
        link_to_ipo = 'https://skill-up.getcourse.ru/teach/control/stream/view/id/788708572'
        await message.bot.send_message(chat_id=chat_id, text=f"{drop_ipo(june_username, sheet_ipo=sheet_ipo,skillup=link_to_ipo, manager=manager_username)}", parse_mode='Markdown')
    else:
        await message.answer('ты не куратор в этом чате, поэтому ты не можешь отправить сообщение')


@router.message(F.text.lower() == 'приглашение в "обучение сотрудников"')
async def invate_to_learn_group(message: Message, state: FSMContext, session: AsyncSession):
    chat_id = await state.get_data()
    chat_id = chat_id['chat_id']
    # data кешурестся в redis name = chat_id + user_id
    data = await info_about_chat(session, int(chat_id), int(message.from_user.id))
    if data:
        june = data['user_id']
        june_username = await message.bot.get_chat(int(june))
        june_username = june_username.username

        link_chat = await message.bot.export_chat_invite_link(chat_id)
        await message.bot.send_message(chat_id=chat_id,text=f'{invate_to_learn_users(june_username)}')
    else:
        await message.answer('ты не куратор в этом чате, поэтому ты не можешь отправить сообщение')



@router.message(F.text.lower() == 'назад')
async def back_to_all_message(message: Message):
    await message.answer('назад', reply_markup=finaly_message_from_junior_key())