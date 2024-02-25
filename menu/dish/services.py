from base.handlers import MessageHandler, CallbackHandler
from menu.dish.states import Dish


class BaseDishAmount:
    async def handle(self, *args, **kwargs):
        await self._state.set_state(Dish.amount)
        await self._message.answer('Enter amount of dish')


class DishAmountCallbackHandler(BaseDishAmount, CallbackHandler):
    pass


class DishAmountMessageHandler(BaseDishAmount, MessageHandler):
    pass


class DishCommentHandler(MessageHandler):
    async def handle(self, *args, **kwargs):
        if not self._is_valid_amount(self._message.text):
            await self._message.answer('Invalid amount of dish')
            from menu.dish.handlers import dish_detail_amount_error_handler
            await dish_detail_amount_error_handler(self._message, **self._data)
            return
        await self._state.set_state(Dish.comment)
        await self._message.answer('Enter comment of dish')

    def _is_valid_amount(self, value: str) -> bool:
        return value.isdigit()


class DishFinishHandler(MessageHandler):
    async def handle(self, *args, **kwargs):
        await self._message.answer('Dish added successfully')
        # todo: 1. send btns for redirect to the category detail, category list
