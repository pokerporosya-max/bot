import time
import random
from aiogram import Router, F
from aiogram.types import Message
from db import get_user, update_cactus, pool

router = Router()

COOLDOWN = 6 * 60 * 60  # 6 часов

@router.message(F.text.lower().contains("полить"))
async def cactus(message: Message):

    user = await get_user(message.from_user.id)

    if not user:
        return await message.answer("❌ Пользователь не найден")

    now = int(time.time())
    last = user["last_cactus"] or 0

    # ⏳ КД
    if now - last < COOLDOWN:
        remaining = COOLDOWN - (now - last)
        hours = remaining // 3600
        minutes = (remaining % 3600) // 60

        return await message.answer(
            f"⏳ Уже поливал\n"
            f"Попробуй через {hours}ч {minutes}м"
        )

    # 🌵 РАНДОМНЫЙ РОСТ 1–12
    grow = random.randint(1, 12)

    await update_cactus(message.from_user.id, grow)

    # 💾 КД в БД
    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE users SET last_cactus=$1 WHERE user_id=$2",
            now,
            message.from_user.id
        )

    # ✅ ОБЯЗАТЕЛЬНЫЙ ОТВЕТ
    await message.answer(f"🌵 Кактус вырос +{grow} см")
