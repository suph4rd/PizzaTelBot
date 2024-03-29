import asyncio

from aiogram import Bot, Dispatcher
from settings.base import TOKEN
from commands.handlers import router as commands_router
from menu.category.handlers import router as category_router


async def main() -> None:
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_routers(commands_router, category_router)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
