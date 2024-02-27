from aiogram.fsm.state import StatesGroup, State


class CuratorUpdate(StatesGroup):
    get_methoo_change_curator = State()
    get_chats = State()
    get_curators = State()
    change_curator = State()
