from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.lower().contains("помощь"))
async def help_cmd(message: Message):

    await message.answer(
        "📌 Команды бота:\n\n"
        "👤 Профиль — статистика\n"
        "🎁 Бонус — ежедневная награда\n"
        "🎮 Игры — список игр\n"
        "🎲 Кубик <ставка> — игра\n"
        "🌵 Полить — рост кактуса\n"
        "📊 Топ — рейтинги игроков\n"
    )
