from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from menu.category.services import CategoryMessageHandler, CategoryDetailCallbackHandler
from menu.category.states import Category
from commands.states import DefaultState
from menu.dish.consts import DishDetailRedirect
from menu.dish.states import Dish

router = Router()


@router.message(DefaultState.base)
async def category_list_handler(message: Message, *args, **kwargs) -> None:
    await CategoryMessageHandler(message, *args, **kwargs).handle()


@router.callback_query(F.data == DishDetailRedirect.category_list[0], Dish.redirect)
async def category_list_redirect_handler(callback_query: CallbackQuery, *args, **kwargs) -> None:
    await CategoryMessageHandler(callback_query.message, *args, **kwargs).handle()


@router.callback_query(F.data.startswith(CategoryMessageHandler.prefix), Category.list)
async def category_detail_handler(callback_query: CallbackQuery, *args, **kwargs) -> None:
    await CategoryDetailCallbackHandler(callback_query, *args, **kwargs).handle()


@router.callback_query(F.data == DishDetailRedirect.category_detail[0], Dish.redirect)
async def category_detail_redirect_handler(callback_query: CallbackQuery, *args, **kwargs) -> None:
    await CategoryDetailCallbackHandler(callback_query,*args, **kwargs).handle()
