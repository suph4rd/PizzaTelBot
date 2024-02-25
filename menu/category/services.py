import re

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


class CategoryDetailCallbackHandler(KeyboardHandler, CallbackHandler):
    prefix = 'detail_category'

    # todo: 1. handle actions (+ - edit)
    #       2. customize dish data as post
    #       3. customize Title of topic [css styles]

    async def handle(self):
        # todo: clean active dish_id
        await self._state.set_state(Category.detail)
        # category_id = self._callback.data.split('|')[1]
        category_id = re.search(CategoryMessageHandler.re_category_id, self._callback.data)
        data = await self._state.get_data()
        data.update({CategoryMessageHandler.category_id: category_id})
        await self._state.set_data(data)

        category = self._get_category(category_id)
        await self._callback.message.answer(f'Category {category}')
        for dish in self._get_dishes():
            inline_markup = self._get_keyboard(dish)
            await self._callback.message.answer('; '.join(
                [str(x) for x in dish.values()]
            ), reply_markup=inline_markup)

    def _get_category(self, category_id):
        return 'Main dish'

    def _get_keyboard(self, dish, *args, **kwargs) -> InlineKeyboardMarkup:
        btn_list = []
        # todo: add if amount 0 else edit, delete
        btn_iterator = ('Add',) if dish['amount'] == 0 else ('Edit', 'Delete')
        for name in btn_iterator:
            btn = InlineKeyboardButton(text=name, callback_data=f'{self.prefix}/dish_name_{name}/dish_id_{dish["id"]}')
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
            'category': '',
            'amount': 0,
        } for x in ('Hachapuri', 'Borsh', 'Cotlet with pure', 'Draniki'))
        dishes[-2]['amount'] = 3
        return dishes
