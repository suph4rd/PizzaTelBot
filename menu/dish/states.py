from aiogram.fsm.state import State, StatesGroup


class Dish(StatesGroup):
    amount = State()
    comment = State()
