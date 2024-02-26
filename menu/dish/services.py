import re

from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.fsm.state import State

from base.dish.handlers import BaseDishCommentHandler, BaseDishAmount, BaseDishList
from base.handlers import MessageHandler, CallbackHandler, KeyboardHandler
from menu.category.services import CategoryMessageHandler
from menu.dish.consts import DishDetailRedirect
from menu.dish.states import Dish


class MenuBaseDishList(BaseDishList, KeyboardHandler):
    prefix = 'menu_dish_list'

    async def pre_handle(self, *args, **kwargs):
        # todo: clean active dish_id
        await self._state.set_state(Dish.list)
        category_id = self._get_category_id()

        data = await self._state.get_data()
        data.update({CategoryMessageHandler.category_id: category_id})
        await self._state.set_data(data)

        category = self._get_category(category_id)
        await self._message.answer(f'Category {category}')

    def _get_category(self, category_id):
        return 'Main dish'

    async def _get_dishes(self):
        gen = (x for x in range(999))
        dishes = tuple({
                           'id': next(gen),
                           'title': x,
                           'description': '',
                           'price': '',
                           'image': '',
                           'category': '',
                           'amount': 0,
                       } for x in ('Margarita', '4 cheese', '4 seasons', 'Seafood'))
        dishes[-2]['amount'] = 3
        return dishes

    def _get_category_id(self):
        raise NotImplementedError


class MenuDishListCallbackHandler(MenuBaseDishList, CallbackHandler):
    def _get_category_id(self):
        category_search = re.search(CategoryMessageHandler.re_category_id, self._callback.data)
        if not category_search:
            raise ValueError('category_id is absent')
        category_data = category_search[0][:-1]
        return int(category_data.split('_')[-1])


class BaseMenuDishAmount(BaseDishAmount):
    def _get_state(self) -> State:
        return Dish.amount

    async def _fail(self, *args, **kwargs):
        from menu.dish.handlers import dish_detail_amount_error_handler
        await dish_detail_amount_error_handler(self._message, **self._data)

    async def _success(self, *args, **kwargs):
        await MenuDishCommentHandler(self._message, **self._data).handle()


class MenuDishAmountCallbackHandler(BaseMenuDishAmount, CallbackHandler):
    pass


class MenuDishAmountMessageHandler(BaseMenuDishAmount, MessageHandler):
    pass


class MenuDishCommentHandler(BaseDishCommentHandler, MessageHandler):
    def _get_state(self) -> State:
        return Dish.comment

    async def _success(self, *args, **kwargs):
        await DishFinishHandler(self._message, **self._data).handle()

    async def _fail(self, *args, **kwargs):
        pass


class DishFinishHandler(KeyboardHandler, MessageHandler):
    async def handle(self, *args, **kwargs):
        await self._state.set_state(Dish.redirect)
        data = await self._state.get_data()
        category_id = data[CategoryMessageHandler.category_id]
        keyboard = self._get_keyboard(category_id)
        await self._message.answer('Dish added successfully', reply_markup=keyboard)

    def _get_keyboard(self, category_id, *args, **kwargs) -> InlineKeyboardMarkup:
        inline_keyboard = []
        for link, title in (DishDetailRedirect.category_list, DishDetailRedirect.dish_list):
            if link == DishDetailRedirect.dish_list[0]:
                link += f'_{category_id}/'
            btn = InlineKeyboardButton(text=title,
                                       callback_data=link)
            inline_keyboard.append([btn])
        inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        return inline_markup


class DishRedirectHandler(CallbackHandler):
    async def handle(self, *args, **kwargs):
        from menu.category.handlers import category_list_redirect_handler
        from menu.dish.handlers import category_detail_redirect_handler
        dish_detail_redirect_function = {
            DishDetailRedirect.category_list[0]: category_list_redirect_handler,
            DishDetailRedirect.dish_list[0]: category_detail_redirect_handler
        }
        func = None
        for key in dish_detail_redirect_function:
            if self._callback.data.startswith(key):
                func = dish_detail_redirect_function[key]
                break
        if not func:
            raise Exception('func is None!')
        await func(self._callback, **self._data)
