from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from base.handlers import KeyboardHandler, BotHandler


class CategoryHandler(KeyboardHandler, BotHandler):
    async def handle(self, *args, **kwargs):
        inline_markup = self._get_keyboard()
        await self._message.reply("Choose the category", reply_markup=inline_markup)

    def _get_keyboard(self) -> InlineKeyboardMarkup:
        inline_keyboard = []
        category_list = self._get_categories()
        for category in category_list:
            btn = InlineKeyboardButton(text=category, callback_data=f'category_{category}')
            inline_keyboard.append([btn])
        inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        return inline_markup

    def _get_categories(self):
        # todo: 1. category request
        #       2. must be async method
        return ('Main dish', 'Soups', 'Salat list', 'Drinks', 'Alcohol drinks')
