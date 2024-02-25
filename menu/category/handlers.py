from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from menu.category.services import CategoryMessageHandler, CategoryDetailCallbackHandler
from menu.category.states import Category
from commands.states import DefaultState

router = Router()


@router.message(DefaultState.base)
async def category_list_handler(message: Message, *args, **kwargs) -> None:
    await CategoryMessageHandler(message, *args, **kwargs).handle()


# F.state == Category.category_list
@router.callback_query(F.data.startswith(CategoryMessageHandler.prefix), Category.list)
async def category_detail_handler(callback_query: CallbackQuery, *args, **kwargs) -> None:
    await CategoryDetailCallbackHandler(callback_query, *args, **kwargs).handle()
