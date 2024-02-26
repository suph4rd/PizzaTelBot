from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.fsm.state import State

from base.handlers import KeyboardHandler, MessageHandler


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


class BaseDishCommentHandler(MessageHandler):
    async def handle(self, *args, **kwargs):
        await self._state.set_state(self._get_state())
        await self._message.answer('Enter comment of dish')

    async def validation_handle(self, *args, **kwargs):
        if self._is_valid_comment(self._message.text):
            await self._success()
            return
        await self._fail()

    def _is_valid_comment(self, value: str) -> bool:
        return True

    def _get_state(self) -> State:
        raise NotImplementedError

    async def _fail(self, *args, **kwargs):
        raise NotImplementedError

    async def _success(self, *args, **kwargs):
        raise NotImplementedError


class BaseDishAmount:
    async def handle(self, *args, **kwargs):
        await self._state.set_state(self._get_state())
        await self._message.answer('Enter amount of dish')

    async def validation_handle(self, *args, **kwargs):
        if self._is_valid_amount(self._message.text):
            await self._success()
            return
        await self._message.answer('Invalid amount of dish')
        await self._fail()

    def _is_valid_amount(self, value: str) -> bool:
        return value.isdigit()

    def _get_state(self) -> State:
        raise NotImplementedError

    async def _fail(self, *args, **kwargs):
        raise NotImplementedError

    async def _success(self, *args, **kwargs):
        raise NotImplementedError
