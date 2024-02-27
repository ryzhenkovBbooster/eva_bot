from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, ScalarResult

from src.db.models import CourseJune, Chat
from src.structure.misc import redis


async def get_old_curator_id(session: AsyncSession, chat_id : int):
    result = await session.execute(select(CourseJune).where(CourseJune.chat == chat_id))
    result: ScalarResult
    user: CourseJune = result.one_or_none()
    if user is None:
        return None
    return user[0].curator
async def update_curator_service(session: AsyncSession, user_id: int, chat_id: int):
    result = await session.execute(update(CourseJune).where(CourseJune.chat == chat_id).values(curator=user_id))

    await session.commit()

    if result.rowcount > 0:
        return True
    else:
        return False



async def get_chats_from_change_curator(session: AsyncSession):
    arr = []

    result = await session.execute(select(Chat).where(Chat.active_chat == True))
    result: ScalarResult
    groups: Chat = result.all()
    for chat in groups:
        chat: Chat
        arr.append(
            {'chatname': chat[0].chatname,
             'chat_id': chat[0].chat_id
             })
    return arr