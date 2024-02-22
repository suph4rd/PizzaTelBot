from aiogram.fsm.state import State, StatesGroup


class Category(StatesGroup):
    category_list = State()
    category_detail = State()
