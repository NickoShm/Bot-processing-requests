import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers.main import router_client
from config import TOKEN
from data_base import create_engine
from middlewares.middleware_db import DataBaseSession
from handlers.admin.main import router_admin
from keyboards import button_menu

bot = Bot(TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def on_startup():
    await button_menu.set_commands(bot)
    await create_engine.create_table()
    print('Бот запущен')


async def on_shutdown():
    print('Бот остановлен')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)

    dp.update.middleware(DataBaseSession(create_engine.session_maker))

    dp.include_router(router_client)
    dp.include_router(router_admin)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR,
                        filename="py_log.log", filemode="w")
    asyncio.run(main())
