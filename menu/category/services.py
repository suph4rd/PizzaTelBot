from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from base.handlers import KeyboardHandler, MessageHandler, CallbackHandler
from .states import Category


class CategoryHandler(KeyboardHandler, MessageHandler):
    prefix = 'list_category_'

    async def handle(self, *args, **kwargs):
        await self._state.set_state(Category.category_list)
        inline_markup = self._get_keyboard()
        await self._message.answer("Choose the category", reply_markup=inline_markup)

    def _get_keyboard(self, *args, **kwargs) -> InlineKeyboardMarkup:
        inline_keyboard = []
        category_list = self._get_categories()
        for category in category_list:
            btn = InlineKeyboardButton(text=category, callback_data=f'{self.prefix}|{category}')
            inline_keyboard.append([btn])
        inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        return inline_markup

    def _get_categories(self) -> tuple:
        # todo: 1. category request
        #       2. must be async method
        return 'Main dish', 'Soups', 'Salat list', 'Drinks', 'Alcohol drinks'


class CategoryDetailHandler(KeyboardHandler, CallbackHandler):
    prefix = 'detail_category_'

    # todo: 1. handle actions (+ - edit)
    #       2. customize dish data as post
    #       3. customize Title of topic [css styles]

    async def handle(self):
        await self._state.set_state(Category.category_detail)
        category = self._callback.data.split('|')[1]
        await self._callback.message.answer(f'Category {category}')
        for dish in self._get_dishes():
            inline_markup = self._get_keyboard(dish['id'])
            await self._callback.message.answer('; '.join(
                [str(x) for x in dish.values()]
            ), reply_markup=inline_markup)

    def _get_keyboard(self, id_, *args, **kwargs) -> InlineKeyboardMarkup:
        btn_list = []
        for name in ('+', '-', 'Edit'):
            btn = InlineKeyboardButton(text=name, callback_data=f'{self.prefix}|{name}|{id_}')
            btn_list.append(btn)
        inline_markup = InlineKeyboardMarkup(inline_keyboard=[btn_list])
        return inline_markup

    def _get_dishes(self) -> tuple:
        gen = (x for x in range(999))
        dishes = tuple({
            'id': next(gen),
            'title': x,
            'description': '',
            'price': '',
            'image': '',
            'category': ''
        } for x in ('Hachapuri', 'Borsh', 'Cotlet with pure', 'Draniki'))
        return dishes
