import time
from aiogram import Router, F
from aiogram.types import Message
from db import get_user, update_balance

router = Router()

COOLDOWN = 24 * 60 * 60  # 24 часа

@router.message(F.text.lower().contains("бонус"))
async def bonus(message: Message):

    user = await get_user(message.from_user.id)
    now = int(time.time())

    if now - user["last_bonus"] < COOLDOWN:
        remaining = COOLDOWN - (now - user["last_bonus"])
        hours = remaining // 3600
        return await message.answer(f"⏳ Бонус уже получен\nПопробуй через {hours}ч")

    await update_balance(message.from_user.id, 2500)

    async with message.bot["db_pool"].acquire() as conn:
        await conn.execute(
            "UPDATE users SET last_bonus=$1 WHERE user_id=$2",
            now,
            message.from_user.id
        )

    await message.answer("🎁 Ты получил бонус +2500 🍬")
