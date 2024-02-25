from aiogram.fsm.state import State, StatesGroup


class Category(StatesGroup):
    list = State()
    detail = State()
