import logging
import asyncio
from aiogram import Bot, Dispatcher

from app.handlers.client import client


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')


async def main():
    bot = Bot(token='')
    dp = Dispatcher()
    dp.include_routers(client)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    logging.info('Bot started up...')


async def shutdown(dispatcher: Dispatcher):
    logging.info('Bot shutting down...')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Bot stopped')
