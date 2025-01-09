import json
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup

from src.structure.misc import redis


def crud_premission():
    kb = ReplyKeyboardBuilder()

    kb.button(text='users')
    kb.button(text='chats')


    return kb.as_markup(resize_keyboard=True)

def users_key():
    kb = ReplyKeyboardBuilder()

    kb.button(text='access')
    kb.button(text='главное меню')

    return kb.as_markup(resize_keyboard=True)

def get_all_from_chat_key(items: list[dict]):
    page = 1
    total_items = len(items)
    page_size = max(1, total_items // 10)  # Автоматический расчет количества элементов на странице
    total_pages = (len(items) + page_size - 1) // page_size  # Рассчитываем количество страниц
    page = max(1, min(page, total_pages))  # Ограничиваем номер страницы в допустимых пределах

    # Получаем элементы для текущей страницы
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_items = items[start_idx:end_idx]

    rows = [[InlineKeyboardButton(text=item['chatname'], callback_data=str(item['chatid']))] for item in items]
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text='⏪ Пред.', callback_data=f'page_{page - 1}'))
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text='След. ⏩', callback_data=f'page_{page + 1}'))

    if nav_buttons:
        rows.append(nav_buttons)

    # Добавляем кнопку 'Отмена' в отдельный ряд
    rows.append([InlineKeyboardButton(text='Отмена', callback_data='back_to_menu')])

    # Создаем клавиатуру без указания row_width, так как каждый ряд уже определен
    return InlineKeyboardMarkup(inline_keyboard=rows)
async def get_all(items: list[dict])-> ReplyKeyboardMarkup:
    keyboard = []
    for item in items:
        redis_key = f"item_data:{item['username']}"
        await redis.set(redis_key, json.dumps(item))

        button = InlineKeyboardButton(text=str(item['username']), callback_data=redis_key)

        keyboard.append([button])
    keyboard.append([InlineKeyboardButton(text='Отмена', callback_data='cancel')])
    # row = [[InlineKeyboardButton(text=str(item['username']),callback_data="str(item)") for item in items], [InlineKeyboardButton(text='Отмена', callback_data='cancel')]]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def edit_access_k():
    kb = [InlineKeyboardButton(text='изменить досутп', callback_data='a'), InlineKeyboardButton(text='Отмена', callback_data='cancel')]

    return InlineKeyboardMarkup(inline_keyboard=[kb])

def get_chats(items: list[str])-> ReplyKeyboardMarkup:


    row = [[InlineKeyboardButton(text=item,callback_data=item) for item in items], [InlineKeyboardButton(text='Отмена', callback_data='cancel')]]

    return InlineKeyboardMarkup(inline_keyboard=row)

def get_active_or_unactive_chats(chats: list[str]) -> ReplyKeyboardMarkup:
    row = [
        [InlineKeyboardButton(text='Активные чаты', callback_data=json.dumps({'data': True})) ],
        [InlineKeyboardButton(text='Не активные чаты', callback_data=json.dumps({'data': False})) ],
        [InlineKeyboardButton(text='Завершенные чаты', callback_data='finaly')],
        [InlineKeyboardButton(text='Отмена', callback_data='back_to_menu')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=row)


def get_chat_key() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='начать КН')
    # kb.button(text='статус КН')
    kb.button(text='главное меню')

    return kb.as_markup(resize_keyboard=True)


def cancel_key():
    row = [[InlineKeyboardButton(text='cancel', callback_data="cancel")]]
    return InlineKeyboardMarkup(inline_keyboard=row)


def restart_add_course_june_key():
    row = [
        # [InlineKeyboardButton(text='cancel', callback_data='cancel')],
           [InlineKeyboardButton(text='заполнить заново', callback_data='again')],
           [InlineKeyboardButton(text='все верно', callback_data='completed')]]
    return InlineKeyboardMarkup(inline_keyboard=row)

def send_practical_task_key(data):
    kb = [[InlineKeyboardButton(text='send practical task', callback_data=data)]]


    # kb.button(text='send practical task')

    return InlineKeyboardMarkup(inline_keyboard=kb)


def sendOtherService(text: str):
    kb = ReplyKeyboardBuilder()

    kb.button(text=text)

    return kb.as_markup(resize_keyboard=True)


def edit_active_chat_key():
    kb = ReplyKeyboardBuilder()

    kb.button(text='Забрать доступы')
    kb.button(text='change curator')
    kb.button(text='Текста для ИС')
    kb.button(text='главное меню')

    return kb.as_markup(resize_keyboard=True)


def finaly_message_from_junior_key():
    kb = ReplyKeyboardBuilder()

    kb.button(text='skill-up правильный')
    kb.button(text='фото, подпись')
    kb.button(text='приглашения')
    kb.button(text='выдача ИПО сотруднику')
    kb.button(text='close')
    kb.button(text='главное меню')




    return kb.as_markup(resize_keyboard=True)
def message_from_create_photo_key():
    kb = ReplyKeyboardBuilder()

    kb.button(text='фото для подписи')
    kb.button(text='инструкция про подпись')
    kb.button(text='фото + девиз')
    kb.button(text='назад')



    return kb.as_markup(resize_keyboard=True)


def message_from_all_invates_key():
    kb = ReplyKeyboardBuilder()

    kb.button(text='приглашение на встречи ИС')
    kb.button(text='приглашение в "Обучение сотрудников"')
    kb.button(text='назад')


    return kb.as_markup(resize_keyboard=True)
