from aiogram import Router
from aiogram.types import Message
from db import update_balance

router = Router()

@router.message(lambda m: m.text.startswith("перевод"))
async def transfer(message: Message):
    parts = message.text.split()

    if len(parts) == 3:
        user_id = int(parts[1])
        amount = int(parts[2])
    else:
        return await message.answer("перевод <ID> <сумма>")

    await update_balance(message.from_user.id, -amount)
    await update_balance(user_id, amount)

    await message.answer(f"💸 Переведено {amount} 🍬")
