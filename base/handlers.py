from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton


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


class BaseDishList(KeyboardHandler):
    prefix: str = None

    # todo: 1. handle actions (+ - edit)
    #       2. customize dish data as post
    #       3. customize Title of topic [css styles]

    async def pre_handle(self, *args, **kwargs):
        pass

    async def post_handle(self, *args, **kwargs):
        pass

    async def handle(self):
        await self.pre_handle()
        dish_list = await self._get_dishes()
        for dish in dish_list:
            inline_markup = self._get_keyboard(dish)
            await self._message.answer('; '.join(
                [str(x) for x in dish.values()]
            ), reply_markup=inline_markup)
        await self.post_handle()

    def _get_keyboard(self, dish, *args, **kwargs) -> InlineKeyboardMarkup:
        # todo: maybe abstract method [callback_data] ???
        btn_list = []
        btn_iterator = ('Add',) if dish['amount'] == 0 else ('Edit', 'Delete')
        for name in btn_iterator:
            btn = InlineKeyboardButton(text=name, callback_data=f'{self.prefix}/dish_name_{name}/dish_id_{dish["id"]}')
            btn_list.append(btn)
        inline_markup = InlineKeyboardMarkup(inline_keyboard=[btn_list])
        return inline_markup

    async def _get_dishes(self):
        raise NotImplementedError
