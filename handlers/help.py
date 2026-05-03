from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "❓ Помощь")
async def help_cmd(message: Message):
    await message.answer(
        "❓ Помощь\n\n"
        "👤 Профиль — статистика игрока\n"
        "🎁 Бонус — ежедневная награда\n"
        "🎮 Игры — список игр\n"
        "🎲 Кубик — игра со ставкой\n"
        "🌵 Полить — рост кактуса\n"
        "📊 Топ — рейтинги игроков"
    )
