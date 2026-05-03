import time
from aiogram import Router, F
from aiogram.types import Message
from db import get_user, update_cactus

router = Router()

COOLDOWN = 6 * 60 * 60  # 6 часов

@router.message(F.text.lower().contains("полить"))
async def cactus(message: Message):

    user = await get_user(message.from_user.id)
    now = int(time.time())

    if now - user["last_cactus"] < COOLDOWN:
        remaining = COOLDOWN - (now - user["last_cactus"])
        hours = remaining // 3600
        return await message.answer(f"⏳ Уже поливал\nПопробуй через {hours}ч")

    grow = 10

    await update_cactus(message.from_user.id, grow)

    async with message.bot["db_pool"].acquire() as conn:
        await conn.execute(
            "UPDATE users SET last_cactus=$1 WHERE user_id=$2",
            now,
            message.from_user.id
        )

    await message.answer(f"🌵 Кактус вырос +{grow} см")
