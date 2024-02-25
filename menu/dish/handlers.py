from aiogram import Router
from aiogram.types import Message, CallbackQuery

from .services import DishAmountCallbackHandler, DishAmountMessageHandler, DishCommentHandler, DishFinishHandler, \
    DishRedirectHandler
from .states import Dish
from ..category.states import Category


router = Router()


@router.callback_query(Category.detail)
async def dish_detail_amount_handler(callback_query: CallbackQuery, *args, **kwargs) -> None:
    await DishAmountCallbackHandler(callback_query, *args, **kwargs).handle()


async def dish_detail_amount_error_handler(message: Message, *args, **kwargs) -> None:
    await DishAmountMessageHandler(message, *args, **kwargs).handle()


@router.message(Dish.amount)
async def dish_detail_comment_handler(message: Message, *args, **kwargs) -> None:
    await DishAmountMessageHandler(message, *args, **kwargs).validation_handle()


@router.message(Dish.comment)
async def dish_detail_comment_handler(message: Message, *args, **kwargs) -> None:
    await DishCommentHandler(message, *args, **kwargs).validation_handle()


@router.callback_query(Dish.redirect)
async def dish_detail_redirect_handler(callback_query: CallbackQuery, *args, **kwargs) -> None:
    await DishRedirectHandler(callback_query, *args, **kwargs).handle()

