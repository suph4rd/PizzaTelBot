from aiogram import Router
from aiogram.types import Message, CallbackQuery

from .services import DishAmountHandler, DishCommentHandler, DishFinishHandler
from .states import Dish
from ..category.states import Category


router = Router()


@router.callback_query(Category.category_detail)
async def dish_detail_amount_handler(message: Message, *args, **kwargs) -> None:
    await DishAmountHandler(message, *args, **kwargs).handle()


@router.message(Dish.dish_detail)
async def dish_detail_comment_handler(callback_query: CallbackQuery, *args, **kwargs) -> None:
    await DishCommentHandler(callback_query, *args, **kwargs).handle()


@router.message(Dish.dish_list)
async def dish_detail_comment_handler(callback_query: CallbackQuery, *args, **kwargs) -> None:
    await DishFinishHandler(callback_query, *args, **kwargs).handle()