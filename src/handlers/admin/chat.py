import datetime
import json

from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.FSM.work_with_chats import Chat_work, Delete_access_services
from src.db.database import sessionmaker
from src.db.models import Chat, CourseJune
from src.filters.guard import UserAccessFilter
from src.keyboards.for_admin import get_all_from_chat_key, get_active_or_unactive_chats, crud_premission, get_chat_key, \
        cancel_key, restart_add_course_june_key
from src.filters.private_chat import PrivateChat
from src.service.admin.chats import get_groups_service, get_active_unactiv_groups_service, \
        get_one_chat_service, edit_username, get_info_about_active_chat, get_finaly_chats_service, \
        get_info_about_finaly_chat_service

from src.service.admin.course_june import attach_user_from_chat_service, create_email_service, \
        create_practical_task_service, check_manager_in_bot, create_personnel_folder_service, check_start_service_in_kn, \
        attach_user_from_course, get_email_june_service, create_june
from src.service.admin.init_course import get_init_data
from src.service.admin.takeback_accesses_from_june import get_accesses_service, remove_access_service

from src.static.course_june.text import start_message, info_message, send_to_manager_ipo
from src.structure.misc import redis
from src.service.admin.chats import get_active_unactiv_groups_service

router = Router()

### функция отмены действия

@router.callback_query(F.data.func(lambda data: json.loads(data).get("page")))
async def handle_pagination(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    data = json.loads(callback.data)
    page = data["page"]
    chat_type = data["type"]

    if chat_type == "active":
        chats = await get_active_unactiv_groups_service(session, True)
    elif chat_type == "unactive":
        chats = await get_active_unactiv_groups_service(session, False)
    elif chat_type == "finaly":
        chats = await get_finaly_chats_service(session)
    else:
        await callback.message.answer("Неизвестный тип чатов.")
        return

    total_pages = (len(chats) + len(chats) // 10 - 1) // (len(chats) // 10)
    keyboard = get_all_from_chat_key(chats, page, total_pages, chat_type)
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(Chat_work.get_chats, F.data =='back_to_menu')
@router.callback_query(Chat_work.get_chats_active_or_unactive, F.data == 'back_to_menu')
@router.callback_query(Chat_work.get_chat, F.data =='back_to_menu')
@router.callback_query(Chat_work.get_active_chat, F.data == 'back_to_menu')
async def back_to_admin_menu(callback: CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.answer('back to menu', reply_markup=crud_premission())



## функция получение всех чатов
@router.message(F.text.lower() == "chats", UserAccessFilter(session_pool=sessionmaker), PrivateChat())
async def get_all_chats(message: Message, session: AsyncSession, state: FSMContext):
        chats = await get_groups_service(session)
        await message.answer(text=f'Все группы в которых когда либо был бот', reply_markup=get_active_or_unactive_chats(chats=chats))
        link = 'https://docs.google.com/document/d/1gH96uhBF2e6f2LUMHZCR8nk6KIobBWfjjbxIiGRT_h0/edit'

        await state.set_state(Chat_work.get_chats)



## функция получение активных чатов
@router.callback_query(Chat_work.get_chats, F.data.func(lambda data: json.loads(data)['data'] ) == True)
async def get_active_chats(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
        chats = await get_active_unactiv_groups_service(session, True)
        total_pages = (len(chats) + 9) // 10
        await callback.message.answer(text='активные чаты', reply_markup=get_all_from_chat_key(chats, 'active', 1, total_pages))
        await state.set_state(Chat_work.get_active_chat)


## функция получение не активных чатов
@router.callback_query(Chat_work.get_chats, F.data.func(lambda data: json.loads(data)['data'] ) == False)
async def get_unactive_chats(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
        chats = await get_active_unactiv_groups_service(session, False)
        total_pages = (len(chats) + 9) // 10
        await callback.message.answer(text='не активные чаты', reply_markup=get_all_from_chat_key(chats, 'unactive', 1, total_pages))
        await state.set_state(Chat_work.get_chat)


@router.callback_query(Chat_work.get_chats, F.data == 'finaly')
async def get_finaly_chats(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
        chats = await get_finaly_chats_service(session)
        total_pages = (len(chats) + 9) // 10
        await callback.message.answer(text='завершенные чаты', reply_markup=get_all_from_chat_key(chats, 'finaly', 1, total_pages))
        await state.set_state(Chat_work.finaly_chats)


@router.callback_query(Chat_work.finaly_chats)
async def get_info_about_finaly_chat(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
        chatname = callback.data
        chat = await get_one_chat_service(session, chatname)
        if chat is None:
                await callback.message.answer('err: чат не найден в базе данных')
        else:
                await get_info_about_finaly_chat_service(callback, session, chat_id=chat['chat_id'])
        await state.clear()



@router.callback_query(Chat_work.get_active_chat)
async def get_one_active_chat(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
        data = await state.get_data()

        if ('curator_changed' in data.keys() and data['curator_changed'] is not True) or 'curator_changed' not in data.keys():

                chatname = callback.data




                chat = await get_one_chat_service(session, chatname)
        else:
                await state.update_data(curator_changed=False)

                chat = {
                        "chat_id": data['chat_id']
                }
        if chat is None:
                await callback.message.answer('err: чат не найден в базе данных')

        else:
                await get_info_about_active_chat(callback, session, chat_id=chat['chat_id'])

        await state.clear()

        await state.set_state(Delete_access_services.select_access)
        await state.update_data(chat_id=chat['chat_id'])


@router.message(F.text.lower() == 'забрать доступы', Delete_access_services.select_access)
async def select_access_services(message: Message, session: AsyncSession, state: FSMContext):
        data = await state.get_data()
        chat_id = data['chat_id']
        results = await remove_access_service(session, chat_id)
        title = await message.bot.get_chat(chat_id=chat_id)
        title = title.title
        if results:
                await message.bot.set_chat_title(chat_id=chat_id, title='Архив ' + str(title))
                response_text = '\n'.join(f"{func_name} returned {'True' if result else 'False'}" for func_name,result in results.items())
                await message.answer(text=response_text)
        else:
                await message.answer(text='false')
        await state.clear()



## функция получение одного чата из выборки активных\неактивных чатов
@router.callback_query(Chat_work.get_chat)
async def get_one_chat(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
        if callback.data == 'cancel':
                data = await state.get_data()
                data = data.get('get_one_chat', None)
        else:

                data = callback.data
                await state.update_data(get_one_chat=data)
        chat = await get_one_chat_service(session, data)
        if chat is not None:
                text = f"Название чата {chat['chatname']}\n ID чата {chat['chat_id']}"
                await callback.message.answer(text=text, reply_markup=get_chat_key())
                # await state.clear()
                await state.update_data(chat_id=chat['chat_id'])
                await state.set_state(Chat_work.create_new_june)
                await state.update_data()
        else:
                await callback.message.answer('такого чата не существует')
                # await state.clear()
## функция инициализцация курса новичка\ получение  имени пользователя телеграма новичка
@router.message(Chat_work.create_new_june, UserAccessFilter(session_pool=sessionmaker))
@router.callback_query(Chat_work.create_new_june, UserAccessFilter(session_pool=sessionmaker))
async def start_kn(message: Message | CallbackQuery, state: FSMContext):
        data = await state.get_data()
        data = data.get('chat_id')
        await state.clear()
        await state.update_data(chat_id=data)
        await message.answer('введите имя пользователя новичка')

        await state.set_state(Chat_work.username)




# @router.message(Chat_work.fullname)
# async def input_fullname(message: Message, state: FSMContext):
#         await message.answer('введите полное имя сотрудника через пробел')
#         await state.update_data(junior=edit_username(message.text))
#         await state.set_state(Chat_work.username)


## функция получения менежера
@router.message(Chat_work.username)
@router.message(F.text.lower() == 'введите имя руководителя', Chat_work.username)
async def input_manager(message: Message | CallbackQuery, state: FSMContext):
        data = await state.get_data()
        data = data.get('junior')
        if data:
                await state.set_state(Chat_work.rangdep)

        else:

                await message.answer('введите имя пользователя руководителя')
                username = message.text
                if '@' in username:
                        username = username.replace('@', '')
                if 'https' in username:
                        username = username.replace('https://t.me/', '')

                await state.update_data(junior=str(username))
                await state.set_state(Chat_work.rangdep)




@router.message(Chat_work.rangdep)
async def rang_dep(message: Message, state: FSMContext, session: AsyncSession):

        username = message.text
        if '@' in username:
                username = username.replace('@', '')
        if 'https' in username:
                username = username.replace('https://t.me/', '')

        manager = await check_manager_in_bot(message,username, session)
        if manager:

                await message.answer(text='введите департамент и отдел кн, в таком формате: div1.dep2')
                await state.update_data(curator=message.text, manager_id=str(manager), manager_name=username)
                await state.set_state(Chat_work.date_init)
        else:
                await message.answer('введите имя руководителя')
                await state.set_state(Chat_work.username)
                await input_manager(message, state)


@router.message(Chat_work.date_init)
async def date_init(message: Message, state: FSMContext):
        await state.update_data(rang=message.text)
        await message.answer('введите дату в формате [ММ-ДД]')
        await state.set_state(Chat_work.check_info)







@router.message(Chat_work.check_info)
async def check_info(message: Message, state: FSMContext, session: AsyncSession):
        data_state = await state.get_data()
        june = data_state.get('junior')
        manager = data_state.get('manager_name')
        rang = data_state.get('rang')
        month_day = message.text.split('-')
        current_year = datetime.datetime.now().year
        formatted_date = datetime.date(year=current_year, month=int(month_day[0]), day=int(month_day[1]))
        await state.update_data(form_date=str(formatted_date))

        await message.answer(f'проверьте:\nновичок: {june}\nруководитель: {manager}\nrang: {rang}\nДата инициализации: {formatted_date}',
                             reply_markup=restart_add_course_june_key())
        # print('username: ', message.from_user.username)




# @router.callback_query(Chat_work.complited)
async def post_start_message_from_chat(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
        # from src.bot import bot
        data = await state.get_data()
        chat_id = data.get('chat_id', None)
        user_id = data.get('junior')
        data_message = user_id
        manager = data.get('manager_name')
        rang = data.get('rang')
        formatted_date = data.get('form_date').split('-')
        formatted_date = datetime.date(year=int(formatted_date[0]), month=int(formatted_date[1]), day=int(formatted_date[2]))


        data = {
                "sender_id": callback.from_user.id,
                "username": data_message,
                "chat_id": chat_id,
                "manager_id": int(data.get('manager_id')),
                "manager": manager,
                "rang": rang,


        }
        if formatted_date == datetime.datetime.now().date():
                data['form_date'] = None
        else:
                data['form_date'] = formatted_date

        attach_user = await attach_user_from_course(session=session, data=data)
        if attach_user:

                if data['form_date'] is None:
                        date_init = str(datetime.date.today()).split('-')
                        date_init = date_init[2] + '-' + date_init[1] + '-' + date_init[0]
                else:
                        date_init = str(formatted_date).split('-')
                        date_init = date_init[2] + '-' + date_init[1] + '-' + date_init[0]

                await callback.bot.send_message(chat_id=chat_id,
                                                text=start_message(data_message, date_init))

                await callback.message.answer(f'Инициализация  {data_message}, завершена.')
                await state.clear()




        else:
                await callback.message.answer('Ошибка при записи в базу данных, на этапе инициализации')






        # await callback.answer(f'ожидаем ответа от {data_message}')
        #

        # print('rang1: ' + rang)
        #
        # await redis.set(chat_id, json.dumps(data), ex=432000)
        # await state.update_data(prev_state=Chat_work.create_new_june, manager=callback.message.text)
        # await state.set_state(Chat_work.check_info)




@router.message(F.text.lower() == 'принято')
async def ready_to_begin(message: Message, session: AsyncSession):
        data = await get_init_data(message, session)
        print(data)
        if data is not None and data['email'] is None and data['username'] == message.from_user.username:
                user_id = message.from_user.id
                await session.execute(
                        update(Chat).where(Chat.chat_id == data['chat_id']).values(user_chat_id=user_id))
                await session.execute(update(CourseJune).where(message.chat.id == data['chat_id']).values(ready_to_begin='True'))
                await session.commit()

                if data['date'] == 'None':
                        return await create_june(message.bot, session, data)
                if data['date'] != 'None':

                        formatted_date = data['date'].split('-')
                        formatted_date = datetime.date(year=int(formatted_date[0]), month=int(formatted_date[1]),
                                                       day=int(formatted_date[2]))
                        data['date'] = formatted_date


                if data['date'] <= datetime.datetime.now().date():

                        await create_june(message.bot, session, data)
                else:
                        formatted_date = str(data['date']).split('-')
                        formatted_date = formatted_date[2] + '-' + formatted_date[1] + '-' + formatted_date[0]
                        await message.answer(f'Отлично, {formatted_date} в 09:00 я пришлю данные для входа в почту, хорошего дня')


        else:
                await redis.delete(str(message.chat.id))
                await message.answer(text=f"@{message.from_user.username} Если вы проходите курс новичка и получаете это сообщение, то напишите куратору")






@router.callback_query(F.data == 'cancel')
async def cancel_oper(callback: CallbackQuery, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
                return
        data = await state.get_data()
        prev_state = data.get('prev_state')
        prev_message=data.get('prev_message')
        print('state: ', prev_state)
        # await callback.message.answer('Операция отменена')
        await state.set_state(prev_state)
        await callback.message.answer(prev_message, reply_markup=cancel_key())

@router.callback_query(F.data == 'again')
async def refractor_data(callback: CallbackQuery, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
                return
        await state.set_state(Chat_work.create_new_june)
        # await state.da
        await start_kn(callback, state)
        await callback.answer('введите имя пользователя новичка')

@router.callback_query(F.data == 'completed')
async def it_true_info(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
        currnet_state = await state.get_state()
        if currnet_state is None:
                return
        await post_start_message_from_chat(callback, state, session)

        



