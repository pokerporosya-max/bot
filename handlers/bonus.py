from aiogram import Router, F
from aiogram.types import Message
from db import update_balance

router = Router()

@router.message(F.text == "🎁 Бонус")
async def bonus(message: Message):
    await update_balance(message.from_user.id, 2500)
    await message.answer("🎁 Вам начислено +2500 🍬")
