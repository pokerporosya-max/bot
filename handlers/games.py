from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "🎮 Игры")
async def games_menu(message: Message):
    await message.answer(
        "🎮 Игры\n\nВыбери игру:\n\n🎲 Кубик"
    )
