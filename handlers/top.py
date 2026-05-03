from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "📊 Топ")
async def top_menu(message: Message):
    await message.answer(
        "🏆 Топ\n\nВыбери категорию:\n\n💰 Баланс\n🎮 Игры\n🌵 Кактус"
    )
