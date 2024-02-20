from enum import Enum

from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Router


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
async def command_start_handler(message: Message) -> None:
    welcome_text = '''Welcome to the Pizza bot!'''
    await message.answer(welcome_text)


@router.message(Command('help'))
async def command_help_handler(message: Message) -> None:
    result = '''Available commands:\n'''
    for command in Commands.values():
        result += f'{command} \n'
    await message.answer(result)
