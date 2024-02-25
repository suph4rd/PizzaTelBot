from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from base.handlers import KeyboardHandler, MessageHandler, CallbackHandler
from .states import Category


class CategoryMessageHandler(KeyboardHandler, MessageHandler):
    prefix = 'list_category'
    category_id = 'category_id'
    re_category_id = 'category_id_\d+/'

    async def handle(self, *args, **kwargs):
        await self._state.set_state(Category.list)
        # todo: clean active category_id/dish_id
        inline_markup = self._get_keyboard()
        await self._message.answer("Choose the category", reply_markup=inline_markup)

    def _get_keyboard(self, *args, **kwargs) -> InlineKeyboardMarkup:
        inline_keyboard = []
        category_list = self._get_categories()
        for category in category_list:
            btn = InlineKeyboardButton(text=category['name'],
                                       callback_data=f'{self.prefix}/category_id_{category["id"]}/')
            inline_keyboard.append([btn])
        inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        return inline_markup

    def _get_categories(self):
        # todo: 1. category request
        #       2. must be async method
        gen = (x for x in range(999))
        return [{'id': next(gen), 'name': x} for x in ('Main dish', 'Soups', 'Salat list', 'Drinks', 'Alcohol drinks')]
