from aiogram.fsm.state import StatesGroup, State


class Chat_work(StatesGroup):
    finaly_chats = State()
    get_active_chat = State()
    get_chats = State()
    get_chats_active_or_unactive = State()
    get_chat = State()
    create_new_june = State()
    manager = State()
    username = State()
    fullname = State()
    rangdep = State()
    check_info = State()
    complited = State()
    date_init = State()


class Delete_access_services(StatesGroup):
    select_access = State()