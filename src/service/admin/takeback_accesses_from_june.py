from aiogram.types import Message
from sqlalchemy import select, ScalarResult, update
from sqlalchemy.ext.asyncio import AsyncSession

from API.bb_platform.bb_platform import delete_user_in_bb
from API.google.drive import remove_folder_by_id_in_dep, remove_folder_by_id_in_personal, remove_folder_by_id_in_IPO
from API.google.googleDirectory import remove_user_by_email
from src.db.models import CourseJune, Chat


async def get_accesses_service(session: AsyncSession, chat_id: int):
    result = await session.execute(select(CourseJune).where(CourseJune.chat == chat_id))
    result: ScalarResult
    data = result.one_or_none()

    if data is None:
        return None
    else:

        data = data[0]
        data = {
            column.name: getattr(data, column.name)
            for column in data.__table__.columns
        }
        return data



async def remove_access_service(session: AsyncSession, chat_id: int):
    data = await get_accesses_service(session, chat_id)
    if data is None:
        return False

    personal_folder_id = data['personal_folder_id']
    user_folder_id = data['user_folder_id']
    email = data['create_email']
    rang = data['rang']
    ipo_folder_id = data['ipo_folder_id']
    # tonnus = data['tonnus']
    await change_status_in_course_june(session, chat_id, 'true')
    remove_google_account = remove_user_by_email(user_key=email)
    remove_personal_folder = remove_folder_by_id_in_personal(personal_folder_id)
    remove_user_folder = remove_folder_by_id_in_dep(user_folder_id, rang)
    remove_ipo_folder = remove_folder_by_id_in_IPO(ipo_folder_id)
    remove_tonnus = delete_user_in_bb(data)
    change_status = await change_status_in_chat(session, chat_id, False)
    if change_status is False:
        return 'err: ошибка при изменении статуса чата'
    result = {
        "remove_google_account": remove_google_account,
        "remove_personal_folder": remove_personal_folder,
        "remove_user_folder": remove_user_folder,
        "remove_ipo_folder": remove_ipo_folder,
        "remove_bb_platform" :  remove_tonnus
    }
    return result

async def change_status_in_chat(session: AsyncSession, chat_id: int, val: bool):
    result = await session.execute(update(Chat).where(Chat.chat_id == chat_id).values(active_chat=val))
    await session.commit()

    ## удалаем данные из кеша

    if result.rowcount > 0:
        return True
    return False


async def change_status_in_course_june(session: AsyncSession, chat_id: int, val: str) -> bool:
    result = await session.execute(update(CourseJune).where(CourseJune.chat == chat_id).values(finaly_stage=val))
    await session.commit()

    ## удалаем данные из кеша

    if result.rowcount > 0:
        return True
    return False
