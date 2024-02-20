import asyncio

from aiogram import Bot, Dispatcher
from settings.base import TOKEN
from commands.handlers import router as commands_router


async def main() -> None:
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_router(commands_router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
