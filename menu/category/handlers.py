from aiogram import Router
from aiogram.types import Message

from menu.category.services import CategoryHandler

router = Router()


@router.message()
async def category_list_handler(message: Message) -> None:
    await CategoryHandler(message).handle()
