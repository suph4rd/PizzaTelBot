class KeyboardHandler:
    def _get_keyboard(self):
        raise NotImplementedError


class BotHandler:
    def __init__(self, message, **kwargs):
        self._message = message
        self._data = kwargs

    async def handle(self, *args, **kwargs):
        raise NotImplementedError()
