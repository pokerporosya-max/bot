from aiogram import Router, F
from db import add

router = Router()


@router.message(F.text.startswith("кубик"))
async def dice(msg):
    d = await msg.answer_dice("🎲")
    v = d.dice.value

    if v in [4, 6]:
        add(msg.from_user.id, "balance", 100)
        await msg.answer("🎉 x2 победа")
    else:
        add(msg.from_user.id, "balance", -50)
        await msg.answer("💀 проигрыш")
