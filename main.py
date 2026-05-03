import asyncio
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from db import init_db

# handlers
from handlers import (
    start,
    profile,
    bonus,
    games,
    dice,
    cactus,
    transfer,
    admin,
    top,
    help,
    about,
    terms
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    # БД
    await init_db()

    # роутеры
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(bonus.router)
    dp.include_router(games.router)
    dp.include_router(dice.router)
    dp.include_router(cactus.router)
    dp.include_router(transfer.router)
    dp.include_router(admin.router)
    dp.include_router(top.router)
    dp.include_router(terms.router)
    dp.include_router(help.router)
    dp.include_router(about.router)

    # запуск
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
