import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

from handlers.profile import router as profile
from handlers.game import router as game
from handlers.game_dice import router as dice

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(profile)
dp.include_router(game)
dp.include_router(dice)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
