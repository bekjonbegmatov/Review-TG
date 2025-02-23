import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from config import bot_tocen  

# Import Routers
from heandlers.main_heandler import router as main_router
from heandlers.code_review_handler import router as code_review_router
from heandlers.tools_handler import router as tools_router
from heandlers.admin.admin_handler import router as admin_router

logging.basicConfig(level=logging.INFO)  # Logging
bot = Bot(token=bot_tocen)  # Conn Bot

dp = Dispatcher()


dp.include_router(admin_router)
dp.include_router(main_router)
dp.include_router(code_review_router)
dp.include_router(tools_router)

async def main():
    await dp.start_polling(bot)  

if __name__ == "__main__":
    asyncio.run(main())
