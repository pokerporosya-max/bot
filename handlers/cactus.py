import random
from aiogram import Router, F
from aiogram.types import Message
from db import update_cactus

router = Router()

@router.message(F.text == "🌵 Полить")
async def cactus(message: Message):

    grow = random.randint(1, 12)

    await update_cactus(message.from_user.id, grow)

    total = grow  # упрощённый вывод

    if total >= 100:
        value = f"{total / 100:.2f} м"
    else:
        value = f"{total} см"

    await message.answer(
        f"🌵 Кактус\n\n+{value}"
    )
