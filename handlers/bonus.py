import time
from aiogram import Router, F
from aiogram.types import Message
from db import get_user, update_balance, pool

router = Router()

COOLDOWN = 24 * 60 * 60

@router.message(F.text.lower().contains("бонус"))
async def bonus(message: Message):

    user = await get_user(message.from_user.id)
    now = int(time.time())

    last = user["last_bonus"] or 0

    if now - last < COOLDOWN:
        return await message.answer("⏳ Бонус уже получен")

    await update_balance(message.from_user.id, 200)

    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE users SET last_bonus=$1 WHERE user_id=$2",
            now,
            message.from_user.id
        )

    await message.answer("🎁 +200 🍬")
