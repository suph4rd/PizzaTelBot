from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext


class KeyboardHandler:
    def _get_keyboard(self, *args, **kwargs):
        raise NotImplementedError


class Handler:
    async def handle(self, *args, **kwargs):
        raise NotImplementedError()


class MessageHandler(Handler):
    def __init__(self, message, *args, **kwargs):
        self._message: Message = message
        self._state: FSMContext = kwargs.get('state')
        self._data = kwargs


class CallbackHandler(Handler):
    def __init__(self, callback, *args, **kwargs):
        self._callback: CallbackQuery = callback
        self._message: Message = callback.message
        self._state: FSMContext = kwargs.get('state')
        self._data = kwargs
