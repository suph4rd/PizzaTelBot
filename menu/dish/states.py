from aiogram.fsm.state import State, StatesGroup


class Dish(StatesGroup):
    list = State()
    amount = State()
    comment = State()
    redirect = State()
