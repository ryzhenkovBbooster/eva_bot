import asyncio
import json
import os
from datetime import datetime

import aioschedule
from aiogram import Bot
from dotenv import load_dotenv
from sqlalchemy.exc import NoResultFound, IntegrityError

from API.google.drive import create_fodler, create_copy_file
from API.google.googleDirectory import create_user_API
from API.skill_up.create_account import createUser_on_skillup
from src.db.models import Chat, CourseJune, Auth
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import update, values, ScalarResult, insert, select

from src.service.admin.access import add_june_indb
from src.static.course_june.text import generate_mail, reg_to_skill_up, create_practical_tasks, start_message
from src.structure.misc import redis



async def preparation(message: Message, session: AsyncSession, column: str):
    check_stage = await check_stage_service(message, session, column)
    if check_stage is False:
        await message.answer(f'Это можно сделать только один раз')

        return False
    if check_stage == 'finaly':
        await message.answer('Курс уже завершен')
        return False
    data = await get_email_june_service(message, session)
    if data is False:
        return False


    return data

async def attach_user_from_course(session: AsyncSession, data):
    try:
        print(data)
        course_june = CourseJune(
            chat=data['chat_id'],
            curator=data['sender_id'],
            manager=data['manager_id'],
            rang=data['rang'],
            date_init=data['form_date']

        )
        await session.merge(course_june)
        await session.commit()
        attach_username = await add_june_indb(session, data['username'])
        if attach_username:
            result = await session.execute(
                update(Chat).where(Chat.chat_id == data['chat_id']).values(username=data['username'], active_chat=True ))
            await session.commit()
            if result:


                return True
            return False
        return False
    except IntegrityError:
        return False


## фукнция инициализация, при начале курса новичка эта функция добалвяет в базу данных информацию нужную для дальнейшей работы
async def attach_user_from_chat_service(session: AsyncSession, data, user_id):
    result = await session.execute(update(Chat).where(Chat.chat_id == data['chat_id']).values(user_chat_id=user_id))
    result: ScalarResult
    await session.commit()
    if result:

        return True


    else:
        return False

# функция которая создает почту в google workspace в ней находится функция которая вызывает метод API который обращается к google admin sdk directory
async def create_email_service(data, message: Message, name: dict):
    create_email = create_user_API(name=name)
    if create_email:
        await message.answer(text=generate_mail(create_email[0], create_email[1]))
        await message.bot.send_message(data['curator'], text='аккунт гугл создан')
        await redis.set(name='google account', value=create_email[0])
        await redis.set(name='fullname', value=create_email[2])
    else:
        await message.answer(text='Произошел сбой, ожидайте')
        await message.bot.send_message(data['sender_id'], text='Произошла ошибка при создании почты')
        await redis.set(name='google account', value='err')

# функция создает skill up, внутри вызывается функция которая исполняет запрос в API getcourse через request запрос
async def create_skillup_service(data, message: Message, bot: Bot):
    # create_skillup = createUser_on_skillup(email, name)
    create_skillup = True
    if create_skillup == True:
        await message.answer(reg_to_skill_up())
    else:
        await message.answer(text='Произошел сбой, ожидайте')
        await bot.send_message(data['sender_id'], text='Произошла ошибка при создании skill up')
##функция которая создает практические задания, внутри нее исполняется функция которая копирует таблицу, создает папку, и помещает в нее копию таблицы
async def create_practical_task_service(data, message: Message, fullname):
    practical_task = create_copy_file(name_copy=fullname)
    print('practical task ',practical_task, type(practical_task))
    if practical_task:
        await message.bot.send_message(data['manager'],text=create_practical_tasks(practical_task[0], practical_task[1]) )
        await message.bot.send_message(data['curator'], text="Файл с практическими заданиями отправлен руководителю")
        await redis.set(name='practical task', value=practical_task[0])
        await redis.set(name='ipo_folder_id', value=practical_task[2])
        await redis.set(name='table_fileid', value=practical_task[3])
    else:
        await message.bot.send_message(data['curator'],
                               text='что то пошло не так, практические заданя не отправлены руководителю')
        await redis.set(name='practical task', value='err')


## функция которая создает папку с личным делом сотрудника на диске в 7 департаменте
async def create_personnel_folder_service(data, message: Message, fullname):
    parent_folder = os.getenv('PERSONNEL_FILES')
    fullname = fullname['familyName'] + ' ' + fullname['givenName']
    folder = create_fodler(parent_folder, fullname)
    if folder:
        await message.bot.send_message(data['curator'], text=f'Папка с личным делом создана\n{folder[0]}')
        await redis.set(name='personnel folder', value='true')
        await redis.set(name='folder_link', value=folder[0])
        await redis.set(name='personal_folder_id', value=folder[1])
    else:
        await message.bot.send_message(data['curator'], text='Ошибка при создании папки с личным делом сотрудника')
        await redis.set(name='personnel folder', value='err')



## функция которая проверяет знает ли бот про руководителя который числится в группе КН
async def check_manager_in_bot(message: Message, data, session: AsyncSession):
    result = await session.execute(select(Auth).where(Auth.username == data))
    result: ScalarResult
    user: Auth = result.one_or_none()
    if user is None:
        await message.answer(f'Такого руководителя нет в нашем боте, отправьте ему мой username: {(await message.bot.me()).username}')
        return False
    else:
        return user[0].user_id

## функция проверяет этапы инициализации КН
async def check_start_service_in_kn(message: Message, data, session: AsyncSession):
    ## получаем данные из кеша для записи в бд
    google_account = await redis.get(name='google account')
    practical_task = await redis.get(name='practical task')
    personnel_folder = await redis.get(name='personnel folder')
    folder_link = await redis.get(name='folder_link')
    fullname = await redis.get(name='fullname')
    personal_folder_id = await redis.get(name='personal_folder_id')
    ipo_folder_id = await redis.get(name='ipo_folder_id')
    table_fileid = await redis.get(name='table_fileid')

    ##обновляем инфу в бд
    result = await session.execute(
        update(CourseJune).where(CourseJune.chat == data['chat_id']).values(
            create_email=str(google_account, 'utf-8'),
            create_personal_folder=str(personnel_folder, 'utf-8'),
            create_practical_task=str(practical_task, 'utf-8'),
            personal_folder_link=str(folder_link, 'utf-8'),
            name_june=str(fullname, 'utf-8'),
            personal_folder_id=str(personal_folder_id, 'utf-8'),
            ipo_folder_id=str(ipo_folder_id, 'utf-8'),
            evaluation_table=str(table_fileid, 'utf-8')




        ))
    await session.commit()


    ## удалаем данные из кеша


    if result.rowcount > 0:

        pass
    else:
        await message.bot.send_message(data['sender_id'], text='Ошибка при записи данных в бд, обратитесь к администратору')
    await redis.delete('folder_link')
    await redis.delete('google account')
    await redis.delete('practical task')
    await redis.delete('personnel folder')
    await redis.delete('fullname')
    await redis.delete('personal_folder_id')
    await redis.delete('ipo_folder_id')
    await redis.delete('table_fileid')


## Получаем данные для выдачи доступов КН записанные в бд, а далее сохраняем их в redis
async def get_email_june_service(message: Message, session: AsyncSession):
       # await redis.delete(str(message.chat.id))

    data_redis = await redis.get(name=str(message.chat.id))
    if not data_redis:



        result = await session.execute(
            select(Chat, CourseJune, Auth)
            .join(CourseJune, Chat.chat_id == CourseJune.chat)
            .join(Auth, CourseJune.manager == Auth.user_id)
            .where(
            Chat.user_chat_id == message.from_user.id, CourseJune.chat == message.chat.id
            ))
        result: ScalarResult
        data = result.all()
        # data = result.one_or_none()
        if data is not None:
            for i, x, z in data:

                chat_data = {
                    key: value for key, value in i.__dict__.items() if not key.startswith('_')
                }
                june_data = {
                    key: value for key, value in x.__dict__.items() if not key.startswith('_')
                }
                auth_data = {
                    key: value for key, value in z.__dict__.items() if not key.startswith('_')

                }

                obj = {
                'email': june_data['create_email'],
                'user_id': chat_data['user_chat_id']

            }

            await redis.set(name=str(chat_data['chat_id']), value=json.dumps({
                'email': june_data['create_email'],
                'user_id': chat_data['user_chat_id'],
                'manager': june_data['manager'],
                'curator': june_data['curator'],
                'practical_tasks': june_data['create_practical_task'],
                'chat_id': chat_data['chat_id'],
                'personal_folder': june_data['personal_folder_link'],
                'name': june_data['name_june'],
                'manager_username': auth_data['username'],
                'rang': june_data['rang'],
                'username': chat_data['username'],



            }))
            data_redis = await redis.get(name=str(message.chat.id))
            data_redis = json.loads(data_redis)
            if data_redis['username'] == message.from_user.username:
                return data_redis
            return False
        else:

            return False
    data_redis = json.loads(data_redis)


    if data_redis['user_id'] == message.from_user.id:
        return data_redis
    else:
        # await message.answer(text='нет доступа!')
        return None


## универсальная функция для обнавления данных в бд в таблице CourseJune
async def add_column_service(message: Message, session: AsyncSession, columnName, status: str):
    value_dict = {
        columnName: status
    }
    await session.execute(update(CourseJune).where(CourseJune.chat == message.chat.id).values(**value_dict))
    await session.commit()
    await redis.delete(str(message.chat.id))
## Проверка стадии выдачи доступов, динамическая, можно использовать для любой стадии после инициализации
async def check_stage_service(message: Message, session: AsyncSession, column_name: str):
    try:

        result = await session.execute(select(CourseJune).where(CourseJune.chat == message.chat.id))
        result: ScalarResult

        june = result.one_or_none()

        if june is not None:

            june: CourseJune
            if june[0].finaly_stage is not None or june[0].finaly_course is not None:
                return 'finaly'
            # if column_name == 'create_practical_task':
            #     return True

            if type(getattr(june[0], column_name)) == type(None):
                return True
            else:
                return False


    except NoResultFound:
        return False

# async def check_other_service(message: Message, session: AsyncSession):
async def finaly_stage_service(session: AsyncSession,chat_id: int ):
    try:

        await session.execute(update(Chat).where(chat_id == Chat.chat_id).values(active_chat=False))
        await session.commit()
        return True
    except Exception as err:
        print("err: ", err)
        return False


async def get_username(session: AsyncSession, user_id: int):
    try:
        result = await session.execute(select(Auth).where(user_id == Auth.user_id))
        result: ScalarResult
        user: Auth = result.one_or_none()
        if user is not None:
            return user[0].username
        else:
            return False
    except Exception as err:
        return False


async def scheduler(bot: Bot, sessionmaker, times: str):
    async def task_wrapper():
        await schedule_job(bot, sessionmaker)  # Вызываем асинхронную функцию напрямую

    # Запланируйте task_wrapper для выполнения, а не schedule_job напрямую
    aioschedule.every().day.at(times).do(task_wrapper)
    while True:
        await aioschedule.run_pending()

        await asyncio.sleep(1)


async def schedule_job(bot: Bot, session_pool: async_sessionmaker):
    async with session_pool() as session:
        async with session.begin():
            curr_date = datetime.now().date()
            data_list = []
            result = await session.execute(
                select(Chat, CourseJune, Auth)
                .join(CourseJune, Chat.chat_id == CourseJune.chat)
                .join(Auth, CourseJune.manager == Auth.user_id)
                .where(CourseJune.date_init == curr_date)
            )
            result: ScalarResult
            data = result.all()
            # data = result.one_or_none()
            if data is not None:
                for i, x, z in data:
                    chat_data = {
                        key: value for key, value in i.__dict__.items() if not key.startswith('_')
                    }
                    june_data = {
                        key: value for key, value in x.__dict__.items() if not key.startswith('_')
                    }
                    auth_data = {
                        key: value for key, value in z.__dict__.items() if not key.startswith('_')

                    }


                    obj = {
                        'chat_id': int(chat_data['chat_id']),
                        'date_init': june_data['date_init'],
                        'username': chat_data['username']


                    }
                    await send_init_message(bot, obj)



async def info_about_chat(session: AsyncSession, chat_id: int, user_id: int) -> dict or bool:
    data = await redis.get(str(chat_id) + str(user_id))
    if data is not None:
        return json.loads(data)
    data = await session.execute(
        select(Chat, CourseJune, Auth)
        .join(CourseJune, Chat.chat_id == CourseJune.chat)
        .join(Auth, CourseJune.manager == Auth.user_id)
        .where(
            Chat.chat_id == chat_id
        ))

    data: ScalarResult
    data = data.all()
    # data = result.one_or_none()
    if data is not None:
        for i, x, z in data:
            chat_data = {
                key: value for key, value in i.__dict__.items() if not key.startswith('_')
            }
            june_data = {
                key: value for key, value in x.__dict__.items() if not key.startswith('_')
            }
            auth_data = {
                key: value for key, value in z.__dict__.items() if not key.startswith('_')

            }



        await redis.set(name=str(chat_data['chat_id']) + str(june_data['curator']), value=json.dumps({
            'email': june_data['create_email'],
            'user_id': chat_data['user_chat_id'],
            'manager': june_data['manager'],
            'curator': june_data['curator'],
            'practical_tasks': june_data['create_practical_task'],
            'chat_id': chat_data['chat_id'],
            'personal_folder': june_data['personal_folder_link'],
            'name': june_data['name_june'],
            'manager_username': auth_data['username'],
            'rang': june_data['rang'],
            'username': chat_data['username'],
            'evo_table': june_data['evaluation_table'],
            'chatname': chat_data['chatname']

        }))
        data_redis = await redis.get(name=str(chat_id) + str(june_data['curator']))
        data_redis = json.loads(data_redis)
        return data_redis
    else:

        return False


    data_redis = json.loads(data_redis)

    if data_redis['user_id'] == message.from_user.id:
        return data_redis
    else:
    # await message.answer(text='нет доступа!')
        return None


async def send_init_message(bot: Bot, data: list):


    await bot.send_message(chat_id=int(data['chat_id']), text=start_message(name=data['username'], date=data['date_init']))