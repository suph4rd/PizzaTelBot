from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from base.handlers import MessageHandler, CallbackHandler, KeyboardHandler
from menu.dish.consts import DISH_DETAIL_REDIRECT_FUNCTION, DishDetailRedirect
from menu.dish.states import Dish


class BaseDishAmount:
    async def handle(self, *args, **kwargs):
        await self._state.set_state(Dish.amount)
        await self._message.answer('Enter amount of dish')

    async def validation_handle(self, *args, **kwargs):
        if not self._is_valid_amount(self._message.text):
            await self._message.answer('Invalid amount of dish')
            from menu.dish.handlers import dish_detail_amount_error_handler
            await dish_detail_amount_error_handler(self._message, **self._data)
            return
        await DishCommentHandler(self._message, **self._data).handle()

    def _is_valid_amount(self, value: str) -> bool:
        return value.isdigit()


class DishAmountCallbackHandler(BaseDishAmount, CallbackHandler):
    pass


class DishAmountMessageHandler(BaseDishAmount, MessageHandler):
    pass


class DishCommentHandler(MessageHandler):
    async def handle(self, *args, **kwargs):
        await self._state.set_state(Dish.comment)
        await self._message.answer('Enter comment of dish')

    async def validation_handle(self, *args, **kwargs):
        await DishFinishHandler(self._message, **self._data).handle()


class DishFinishHandler(KeyboardHandler, MessageHandler):
    async def handle(self, *args, **kwargs):
        keyboard = self._get_keyboard()
        await self._message.answer('Dish added successfully', reply_markup=keyboard)

    def _get_keyboard(self, *args, **kwargs) -> InlineKeyboardMarkup:
        inline_keyboard = []
        for link, title in (DishDetailRedirect.category_list, DishDetailRedirect.category_detail):
            btn = InlineKeyboardButton(text=title,
                                       callback_data=link)
            inline_keyboard.append([btn])
        inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        return inline_markup


class DishRedirectHandler(CallbackHandler):
    async def handle(self, *args, **kwargs):
        data = self._callback.data
        func = DISH_DETAIL_REDIRECT_FUNCTION[data]
        await func(self._message, **self._data)
