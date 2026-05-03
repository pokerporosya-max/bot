import random
from aiogram import Router, F
from aiogram.types import Message
from db import update_cactus

router = Router()

@router.message(F.text.lower() == "полить")
async def cactus(message: Message):

    grow = random.randint(1, 12)

    await update_cactus(message.from_user.id, grow)

    if grow >= 100:
        value = f"{grow / 100:.2f} м"
    else:
        value = f"{grow} см"

    await message.answer(f"🌵 Кактус +{value}")
