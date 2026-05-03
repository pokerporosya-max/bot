from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from db import get_user

router = Router()

# 📌 ПРОФИЛЬ (группа текстом)
@router.message(F.text.lower() == "профиль")
async def profile_text(message: Message):
    await send_profile(message)

# 📌 ПРОФИЛЬ (кнопка в ЛС)
@router.callback_query(F.data == "profile")
async def profile_button(callback: CallbackQuery):
    await send_profile(callback.message)
    await callback.answer()

# 📌 ОБЩАЯ ФУНКЦИЯ
async def send_profile(message: Message):

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
