from aiogram.fsm.state import State, StatesGroup


class Dish(StatesGroup):
    dish_list = State()
    dish_detail = State()
