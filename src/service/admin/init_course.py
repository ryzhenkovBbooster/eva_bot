import json

from aiogram.types import Message
from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Chat, CourseJune, Auth
from src.structure.misc import redis


async def get_init_data(message: Message, session: AsyncSession):
    # await redis.delete(str(message.chat.id))

    data_redis = await redis.get(name=str(message.chat.id))
    if not data_redis:

        result = await session.execute(
            select(Chat, CourseJune, Auth)
            .join(CourseJune, Chat.chat_id == CourseJune.chat)
            .join(Auth, CourseJune.manager == Auth.user_id)
            .where(
                Chat.username == message.from_user.username, CourseJune.chat == message.chat.id
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

            await redis.set(name=chat_data['chat_id'], value=json.dumps({
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
                'date': str(june_data['date_init']),
                'chatname': chat_data['chatname']

            }))
            data_redis = await redis.get(name=str(message.chat.id))
            data_redis = json.loads(data_redis)
            if data_redis['username'] == message.from_user.username:
                return data_redis
            return None
        else:

            return None
    data_redis = json.loads(data_redis)

    if data_redis['username'] == message.from_user.username:
        return data_redis
    else:
        # await message.answer(text='нет доступа!')
        return None