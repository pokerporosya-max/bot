import random
from aiogram import Router
from aiogram.types import Message
from db import update_balance, update_game

router = Router()

@router.message(lambda m: m.text.startswith("кубик"))
async def dice(message: Message):
    try:
        bet = int(message.text.split()[1])
    except:
        return await message.answer("Используй: кубик <ставка>")

    roll = random.randint(1, 6)

    if roll in [4, 6]:
        win = bet * 2
        await update_balance(message.from_user.id, win)
        await update_game(message.from_user.id, True)

        await message.answer(f"🎲 {roll}\n🎉 Победа +{win} 🍬")
    else:
        await update_balance(message.from_user.id, -bet)
        await update_game(message.from_user.id, False)

        await message.answer(f"🎲 {roll}\n💀 Проигрыш -{bet} 🍬")
