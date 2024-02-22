from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from menu.category.services import CategoryHandler, CategoryDetailHandler

router = Router()


@router.message()
async def category_list_handler(message: Message, *args, **kwargs) -> None:
    await CategoryHandler(message, *args, **kwargs).handle()


# F.state == Category.category_list
@router.callback_query(F.data.startswith(CategoryHandler.prefix))
async def category_detail_handler(callback_query: CallbackQuery, *args, **kwargs) -> None:
    await CategoryDetailHandler(callback_query, *args, **kwargs).handle()
