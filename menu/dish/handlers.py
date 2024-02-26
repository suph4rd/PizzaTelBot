from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from .consts import DishDetailRedirect
from .services import MenuDishAmountCallbackHandler, MenuDishAmountMessageHandler, MenuDishCommentHandler, \
    DishRedirectHandler, MenuDishListCallbackHandler
from .states import Dish
from ..category.services import CategoryMessageHandler
from ..category.states import Category


router = Router()


@router.callback_query(F.data.startswith(CategoryMessageHandler.prefix), Category.list)
async def category_detail_handler(callback_query: CallbackQuery, *args, **kwargs) -> None:
    await MenuDishListCallbackHandler(callback_query, *args, **kwargs).handle()


@router.callback_query(F.data == DishDetailRedirect.dish_list[0], Dish.redirect)
async def category_detail_redirect_handler(callback_query: CallbackQuery, *args, **kwargs) -> None:
    await MenuDishListCallbackHandler(callback_query,*args, **kwargs).handle()


@router.callback_query(Dish.list)
async def dish_detail_amount_handler(callback_query: CallbackQuery, *args, **kwargs) -> None:
    await MenuDishAmountCallbackHandler(callback_query, *args, **kwargs).handle()


async def dish_detail_amount_error_handler(message: Message, *args, **kwargs) -> None:
    await MenuDishAmountMessageHandler(message, *args, **kwargs).handle()


@router.message(Dish.amount)
async def dish_detail_comment_handler(message: Message, *args, **kwargs) -> None:
    await MenuDishAmountMessageHandler(message, *args, **kwargs).validation_handle()


@router.message(Dish.comment)
async def dish_detail_comment_handler(message: Message, *args, **kwargs) -> None:
    await MenuDishCommentHandler(message, *args, **kwargs).validation_handle()


@router.callback_query(Dish.redirect)
async def dish_detail_redirect_handler(callback_query: CallbackQuery, *args, **kwargs) -> None:
    await DishRedirectHandler(callback_query, *args, **kwargs).handle()
