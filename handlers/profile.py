from aiogram import Router
from aiogram.types import Message
from db import get_user

router = Router()

@router.message(lambda m: m.text == "👤 Профиль")
async def profile(message: Message):
    user = await get_user(message.from_user.id)

    await message.answer(
f"""👤 Профиль

Имя: @{user['username']}
ID: {user['user_id']}

💰 Баланс: {user['balance']} 🍬
🌵 Кактус: {user['cactus']}

🎮 Сыграно: {user['games']}
🏆 Победы: {user['wins']}
💀 Поражения: {user['loses']}
"""
    )
