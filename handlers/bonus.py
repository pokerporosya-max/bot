import time
from aiogram import Router, F
from aiogram.types import Message
from db import get_user, update_balance, pool

router = Router()

COOLDOWN = 24 * 60 * 60  # 24 часа

@router.message(F.text.lower().contains("бонус"))
async def bonus(message: Message):

    user = await get_user(message.from_user.id)

    if not user:
        return await message.answer("❌ Пользователь не найден")

    now = int(time.time())
    last = user["last_bonus"] or 0

    # ⏳ КД проверка
    if now - last < COOLDOWN:
        remaining = COOLDOWN - (now - last)
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60

        return await message.answer(
            f"⏳ Бонус уже получен\n"
            f"Попробуй через {hours}ч {minutes}м"
        )

    # 💰 выдача
    await update_balance(message.from_user.id, 200)

    # 💾 обновление КД
    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE users SET last_bonus=$1 WHERE user_id=$2",
            now,
            message.from_user.id
        )

    # ✅ ОБЯЗАТЕЛЬНЫЙ ОТВЕТ
    await message.answer("🎁 Ты получил +200 🍬 бонус!")
