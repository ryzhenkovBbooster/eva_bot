import json

from sqlalchemy import select, ScalarResult
from aiogram import Router, F
import ast
from aiogram.filters import Command

from API.bb_platform.bb_platform import create_user_in_bb
from API.google.googleDirectory import rename_account_google_api
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.db.models import Auth
from API.test.post_test import post_test_api, get_tests
from API.google.drive import create_fodler
from src.keyboards.for_admin import send_practical_task_key, sendOtherService
from API.google.dict_orgEmail import obj
from src.service.admin.chats import check_user_in_chat
from src.static.course_june.text import access_to_practical_task, finaly_course_june, rename_email_static, \
    create_lastpass_folder, create_folder_on_drive, reg_to_skill_up, message_from_given_practical_task, \
    send_to_manager_ipo
from src.service.admin.course_june import get_email_june_service, createUser_on_skillup, preparation, \
    add_column_service, finaly_stage_service, get_username
from src.structure.misc import redis
from API.timedoctor.methods_timedoctor import inviteUser

router = Router()

@router.message(F.text.lower() == 'тест')
async def post_tests(message: Message, session: AsyncSession):
    ## словарь с инфой по конкретному кн
    data = await preparation(message=message, session=session, column='hr_tests')
    if data:

        email = data['email']
        curator = data['curator']
        june = message.from_user.username

        send_tests = post_test_api(email)
        if send_tests is not False:
            await message.answer(f'@{june}\n'
                                 f'Ваши тесты\n'
                                 f'Тест на личностные качества:  отправлен на почту\n'
                                 f'Тест IQ: Можно пройти по этой ссылке: https://onlinetestpad.com/t/test-iq-bbooster')
            # await message.bot.send_message(curator, f'тесты для {email}, отправлены')
            await add_column_service(message, session, 'hr_tests', 'true')

        else:

            await message.bot.send_message(curator, f'ошибка при отправке тестов для {email}\nЛог ошибки {send_tests}')

@router.message(F.text.lower() == 'тесты выполнены')
async def add_tests_to_folder(message: Message, session: AsyncSession):
    data = await preparation(message=message, session=session, column='test_completed')
    if data:
        folder_link = data['personal_folder']
        email = data['email']
        curator = data['curator']
        tests: tuple or str or bool = get_tests(email) ## (logis, tools) or tests is not completed or False

        if tests == 'tests is not completed':
            await message.answer('ты еще не закончил тесты, проверь все еще раз, но если это так и есть, тогда напиши куратору')
        elif tests is not False:
            await add_column_service(message, session, 'test_completed', 'true')

            await message.answer('Спасибо, тесты отправлены куратору')
            await message.bot.send_message(curator,
                                           text=f'Новичок из чата {message.chat.title} заполнил тесты\nСсылка: {folder_link}\nTOOLS: {tests[1]}\nLOGIS: {tests[0]}')

        else:
            await message.answer('Спасибо, тесты отправлены куратору')
            await message.bot.send_message(curator, text='При получении результатов теста произошла ошибка, пожалуйста проверь все ручками)')


@router.message(F.text.lower() == 'выдать тд')
async def create_time_doctor(message: Message, session: AsyncSession):
    data = await preparation(message, session, 'time_doctor')
    if data:
        curator = data['curator']
        chat_id = data['chat_id']
        link = await message.bot.export_chat_invite_link(chat_id=chat_id)
        await message.answer('ожидайте ответа куратора, скоро time doctor будет выдан')
        await message.bot.send_message(curator, text=f'Новичок из чата {link}\n'
                                                     f'Просит выдать доступ к timedoctor')

        await add_column_service(message, session, 'time_doctor', 'true')




    #
@router.message(F.text.lower() == 'выдай доступ в bb platform')
async def create_platform(message: Message, session: AsyncSession):
    data = await preparation(message, session, 'tonnus')
    if data:
        data['firstName'] = message.chat.title.split(" ")[1]
        data['lastName'] = message.chat.title.split(" ")[2]
        data['username'] = message.from_user.username
        user = create_user_in_bb(data)
        if user:
            await message.bot.send_message(chat_id=message.chat.id, text=f'@{data["username"]} Аккаунт создан - ссылка для входа https://my.bbooster.io/login\nЛогин: {user["email"]}\nПароль: {user["password"]}')
            await add_column_service(message, session, 'tonnus', 'true')

        else:
            await message.bot.send_message(chat_id=message.chat.id, text=f'Ошибка при создании аккаунта bb platform, ожидайте ответа от куратора')
            await message.bot.send_message(chat_id=int(data['curator']), text=f'Ошибка при создании bb platform у @{message.from_user.username}')
@router.message(F.text.lower() == 'получить практические задания')
async def get_practical_tasks(message: Message, session: AsyncSession):
    data = await preparation(message, session, 'check_practical_task')
    if data:
        curator = data['curator']
        chat_id = data['chat_id']
        sheet_link = data['practical_tasks']
        manager = data['manager']
        manager_username = data['manager_username']
        name_june = data['name']


        link = await message.bot.export_chat_invite_link(chat_id=message.chat.id)




        await message.bot.send_message(
            curator,
            text=f'Новичок из чата {message.chat.title} запросил практическое задание\n'
                 f'ссылка на чат {link}\n'
                 f'ссылка на таблцицу {sheet_link}',
            )
        await message.bot.send_message(curator, text=message_from_given_practical_task(f'@{message.from_user.username}', manager_username, sheet_link ), parse_mode='Markdown')
        await add_column_service(message, session, 'check_practical_task', 'true')

        await message.answer(text='ожидайте ответа куратора, скоро задания будут высланы')




# @router.callback_query(F.data.startswith('task'))
# async def send_practical_task(callback: CallbackQuery):
#
#     chat_id = callback.data.replace('task', '')
#     chat_id = int(chat_id)
#     data = await redis.get(name=chat_id)
#
#     if data:
#         data = data.decode('utf-8')
#         data = json.loads(data)
#         manager = data['manager_username']
#
#         link = data['practical_tasks']
#
#         await callback.bot.send_message(
#             data['user_id'],
#             text=access_to_practical_task(link, manager))
#
#     else:
#         await callback.answer('что-то пошло не так :)')
#

@router.message(F.text.lower() == 'доступ к getcourse')
async def create_getcourse(message: Message, session: AsyncSession):
    data = await preparation(message, session, 'getcourse')
    if data:
        curator = data['curator']
        email = data['email']

        await message.bot.send_message(curator,
                                       text=
                                        f'Новичок в чате {message.chat.title}, запросил доступ к ГК\n'
                                        f'Сcылка на создание юзера: https://my.bbooster.online/pl/user/user/create\n'
                                        f'first name: {message.chat.title.split(" ")[1]} \n'
                                        f'last name:{message.chat.title.split(" ")[2]} \n'
                                        f'email: {email}\n'
                                        f'Ссылка на добавление его в менеджеры если нужно: https://my.bbooster.online/sales/control/participant/new/type/manager\n'
                                        f'Ссылка на реестр ГК: https://docs.google.com/spreadsheets/d/15PhrQ-9tla9KsiS--C025zY3NYbxZB_kNLEfDMWQEvs/edit#gid=1116907708'
                                       )

        await add_column_service(message,session,'getcourse', 'true')


@router.message(F.text.lower() == 'last stage')
async def completed_second_stage(message: Message):
    await message.answer(finaly_course_june())

@router.message(F.text.lower() == 'выдай адрес основной почты')
async def rename_email(message: Message, session: AsyncSession):
    data = await preparation(message, session, 'rename_email')
    if data:

        email = data['email']
        curator = data['curator']
        rang = data['rang']
        sheet_link = data['practical_tasks']
        manager = data['manager']





        rename = rename_account_google_api(email, position=rang)
        if rename:

            curator_username = await message.bot.get_chat(chat_id=curator)
            await message.answer(rename_email_static(f'@{message.from_user.username}', rename, oldEmail=email, username=curator_username.username))
            await add_column_service(message,session,'rename_email', 'true')

        else:
            await message.bot.send_message(curator, text=f'ошибка при переименовании почты пользователя {email}')
        await message.bot.send_message(manager, text=send_to_manager_ipo(link=sheet_link), parse_mode='Markdown')

@router.message(F.text.lower() == "получить доступ к lastpass")
async def lastpass_folder_create(message: Message, session: AsyncSession):
    data = await preparation(message, session, 'lastpass')
    if data:
        curator = data['curator']
        chat_id = data['chat_id']
        link = await message.bot.export_chat_invite_link(chat_id=chat_id)
        await message.bot.send_message(curator, text=f'Новичок из чата {link}\n'
                                                     f'Просит выдать доступ к lastpass')
        await message.answer('Куратор скоро напишет вам')
        await add_column_service(message, session, 'lastpass', 'true')


@router.message(F.text.lower() == 'получить доступ к личной папке')
async def create_folder_gdrive(message: Message, session: AsyncSession):
    data = await preparation(message, session, 'user_folder')
    if data:
        title = message.chat.title
        rang = data['rang']
        div = rang.split('.')[0]
        name = f'{title.split()[1]} {title.split()[2]} BBMC'
        folder = create_fodler(obj[div]['folder'], name_folder=name)
        if folder:

            await message.answer(create_folder_on_drive(folder[0]))
            await add_column_service(message,session,'user_folder', 'true')
            await add_column_service(message, session, 'user_folder_id', folder[1])

        else:
            await message.answer('err: create fodler in google drive')
@router.message(F.text.lower() == "получить доступ к tonnus")
async def create_acc_tonnus(message: Message):
    account = True
    if account:
        await message.answer('tonnus создан')
    else:
        await message.answer('err: create account tonnus')
@router.message(F.text == 'get_email')
async def get_email(message: Message, session: AsyncSession):
    res = await get_email_june_service(message, session)
    print('result: ',type(res))
    await message.answer(text=f'{res}')

## Создание аккаунта на skill-up + добавления в группу обучение
@router.message(F.text.lower() == 'почта создана')
async def create_skillup(message: Message, session: AsyncSession):
    data = await preparation(message, session, 'create_skillup')
    if data:
    ## функция возвращает словарь содержащий
    # {'email': почта пользователя,
    # 'user_id': id пользователя
        email = data['email']
        name = message.chat.title
        name = {
            'first': name.split()[2],
            'last': name.split()[1]
        }

        res = createUser_on_skillup(email, name)
        if res:
            await add_column_service(message,session,'create_skillup', 'true')
            await message.answer(text=reg_to_skill_up())
        else:
            await add_column_service(message, session, 'create_skillup', 'err')




        # await message:




@router.message(F.text.lower() == 'гк создан')
async def gk_complited(message: Message):
    await message.answer()

# @router.message(F.text.lower() == 'курс завершен')
async def finaly_stage(message: Message, session: AsyncSession):
    data = await preparation(message, session, 'finaly_stage')
    print(data)
    if data:
        user = message.from_user.id

        active_chat_id = data['chat_id']
        curator = data['curator']

        close_active_chat = await finaly_stage_service(session, active_chat_id)

        if close_active_chat:
            link = await message.bot.export_chat_invite_link(active_chat_id)
            await message.bot.send_message(curator, text=f'Новичек из чата завершил КН\n{link}')
            # await message.answer('Поздравляю, куратор скоко свяжется с вами')

            await add_column_service(message, session, 'finaly_stage', 'true')



@router.message(F.text.lower() == 'курс новичка пройден')
async def complete_course(message: Message, session: AsyncSession):
    data = await preparation(message, session, 'finaly_course')
    if data:
        curator = data['curator']
        link = await message.bot.export_chat_invite_link(chat_id=message.chat.id)

        await message.bot.send_message(chat_id=curator, text=f'@{message.from_user.username} завершил КН\n{link}')
        await message.answer('После того как куратор проверит задания, он отпишет в чат по дальнейшим действиям')


        await add_column_service(message, session, 'finaly_stage', 'true')
