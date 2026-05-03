import random
from aiogram import Router, F
from aiogram.types import Message
from db import update_balance, update_game

router = Router()

@router.message(F.text.startswith("кубик,Кубик"))
async def dice_game(message: Message):

    parts = message.text.split()

    if len(parts) < 2:
        return await message.answer("Используй: кубик <ставка>")

    try:
        bet = int(parts[1])
    except:
        return await message.answer("Ставка должна быть числом")

    # отправляем "бросок"
    dice_msg = await message.answer_dice(emoji="🎲")
    roll = dice_msg.dice.value

    # победа
    if roll in [4, 6]:
        win = bet * 2

        await update_balance(message.from_user.id, win)
        await update_game(message.from_user.id, win=True)

        await message.answer(f"🎲 Выпало: {roll}\n🎉 Победа +{win} 🍬")

    else:
        await update_balance(message.from_user.id, -bet)
        await update_game(message.from_user.id, win=False)

        await message.answer(f"🎲 Выпало: {roll}\n💀 Проигрыш -{bet} 🍬")
