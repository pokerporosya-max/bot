from aiogram import Router, F
from aiogram.types import Message
from db import get_user

router = Router()

# 👤 ПРОФИЛЬ (из группы и ЛС через кнопку)
@router.message(F.text == "👤 Профиль")
async def profile(message: Message):

    user = await get_user(message.from_user.id)

    if not user:
        return await message.answer("❌ Профиль не найден")

    cactus_value = user["cactus"]

    if cactus_value >= 100:
        cactus_text = f"{cactus_value / 100:.2f} м"
    else:
        cactus_text = f"{cactus_value} см"

    text = (
        f"👤 Профиль\n\n"
        f"Имя: @{user['username']}\n"
        f"ID: {user['user_id']}\n\n"
        f"💰 Баланс: {user['balance']} 🍬\n"
        f"🌵 Кактус: {cactus_text}\n\n"
        f"🎮 Сыграно: {user['games']}\n"
        f"🏆 Победы: {user['wins']}\n"
        f"💀 Поражения: {user['loses']}"
    )

    await message.answer(text)
