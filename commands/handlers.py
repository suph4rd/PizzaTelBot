from enum import Enum

from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Router

from base.utils import get_storage
from menu.category.handlers import category_list_handler
from aiogram.fsm.context import FSMContext
from .states import DefaultState


router = Router()


class Commands(Enum):
    start = '/start'
    help = '/help'

    @classmethod
    def values(cls):
        if not hasattr(cls, '_values_list'):
            cls._values_list = [x.value for x in cls]
        return cls._values_list


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext, *args, **kwargs) -> None:
    welcome_text = '''Welcome to the Pizza bot!'''
    user_data = get_or_create(message)
    storage = get_storage()
    # todo: send request to api
    await storage.set_data(user_data['user_id'], {'user_data': user_data})
    await message.answer(welcome_text)
    await state.set_state(DefaultState.base)
    await category_list_handler(message, state=state, *args, **kwargs)


def get_or_create(message):
    user = message.from_user
    return {
        'username': user.username,
        'user_id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_block': False,
        'url': user.url,
    }


@router.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    result = 'Available commands:\n'
    for command in Commands.values():
        result += f'{command} \n'
    await message.answer(result)
