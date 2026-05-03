import random
from aiogram import Router, F
from aiogram.types import Message
from db import add_cactus

router = Router()

@router.message(F.text == "🌵 Полить")
async def cactus(message: Message):

    grow = random.randint(1, 12)

    await add_cactus(message.from_user.id, grow)

    # формат вывода
    if grow + 0 >= 100:
        value = f"{(grow + 0) / 100:.2f} м"
    else:
        value = f"{grow} см"

    await message.answer(
        f"🌵 Кактус полить\n\n"
        f"+{value}"
    )
