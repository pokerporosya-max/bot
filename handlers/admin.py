from aiogram import Router
from aiogram.types import Message
from config import ADMIN_ID
from db import update_balance

router = Router()

@router.message(lambda m: m.from_user.id == ADMIN_ID and m.text.startswith("выдать"))
async def give(message: Message):
    parts = message.text.split()

    user_id = int(parts[1])
    amount = int(parts[2])

    await update_balance(user_id, amount)

    await message.bot.send_message(
        user_id,
        f"👑 Вам начислено от администратора +{amount} 🍬"
    )

    await message.answer("✅ Выдано")
