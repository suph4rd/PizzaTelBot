from base.handlers import MessageHandler, CallbackHandler
from menu.dish.states import Dish


class DishAmountHandler(CallbackHandler):
    async def handle(self, *args, **kwargs):
        await self._state.set_state(Dish.dish_detail)
        await self._callback.message.answer('Enter amount of dish')


class DishCommentHandler(MessageHandler):
    async def handle(self, *args, **kwargs):
        if not self._is_valid_amount(self._message.text):
            await self._message.answer('Invalid amount of dish')
            from menu.dish.handlers import dish_detail_amount_handler
            await dish_detail_amount_handler(*args, **kwargs)
            return
        await self._state.set_state(Dish.dish_list)
        await self._message.answer('Enter comment of dish')

    def _is_valid_amount(self, value: str) -> bool:
        return value.isdigit()


class DishFinishHandler(MessageHandler):
    async def handle(self, *args, **kwargs):
        await self._message.answer('Dish added successfully')
        # todo: call category detail
