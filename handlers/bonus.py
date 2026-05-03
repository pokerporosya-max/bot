import time
from aiogram import Router, F
from aiogram.types import Message
from db import get_user, update_balance, pool

router = Router()

COOLDOWN = 24 * 60 * 60

@router.message(F.text)
async def bonus(message: Message):

    text = message.text.lower()

    if "бонус" not in text:
        return

    user = await get_user(message.from_user.id)

    if not user:
        return await message.answer("❌ Пользователь не найден")

    now = int(time.time())
    last = user["last_bonus"] or 0

    # ⏳ КД
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

    # 💾 КД запись
    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE users SET last_bonus=$1 WHERE user_id=$2",
            now,
            message.from_user.id
        )

    # ✅ ответ всегда в конце
    await message.answer("🎁 +200 🍬 бонус получен!")
