import time
from aiogram import Router, F
from aiogram.types import Message
from db import get_user, update_cactus, pool

router = Router()

COOLDOWN = 6 * 60 * 60

@router.message(F.text.lower().contains("полить"))
async def cactus(message: Message):

    user = await get_user(message.from_user.id)
    now = int(time.time())

    last = user["last_cactus"] or 0

    if now - last < COOLDOWN:
        return await message.answer("⏳ Уже поливал")

    await update_cactus(message.from_user.id, 10)

    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE users SET last_cactus=$1 WHERE user_id=$2",
            now,
            message.from_user.id
        )

    await message.answer("🌵 +10 см")
