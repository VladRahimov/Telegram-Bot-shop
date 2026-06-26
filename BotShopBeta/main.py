import asyncio

from aiogram import Bot
from aiogram import Dispatcher

from config import TOKEN
from botcommands import set_bot_commands

from database import init_db

from handlers.start import router as start_router
from handlers.buy import router as buy_router
from handlers.text_handler import router as text_router
from handlers.payment import router as payment_router
from handlers.reviev import router as review_router

from handlers.admin import router as admin_router
from handlers.orders import router as orders_router
from handlers.accounts import router as accounts_router
from handlers.stock import router as stock_router



bot = Bot(token=TOKEN)

dp = Dispatcher()




async def main():
    init_db()

    await set_bot_commands(bot)


    dp.include_router(start_router)
    dp.include_router(buy_router)
    dp.include_router(accounts_router)
    dp.include_router(payment_router)
    dp.include_router(review_router)
    dp.include_router(orders_router)
    dp.include_router(stock_router)
    dp.include_router(admin_router)
    dp.include_router(text_router)
    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())