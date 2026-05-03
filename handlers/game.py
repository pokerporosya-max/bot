from aiogram import Router, F
from services import bonus, water, fap, exchange
from db import add

router = Router()


@router.message(F.text == "💰 Бонус")
async def b(msg):
    await msg.answer(f"🎁 +{bonus(msg.from_user.id)} 💰")


@router.message(F.text == "🌵 Полить")
async def w(msg):
    await msg.answer(f"🌵 +{water(msg.from_user.id)} см")


@router.message(F.text == "🧴 Фап")
async def f(msg):
    if fap(msg.from_user.id):
        await msg.answer("🧴 +1 фап")
    else:
        await msg.answer("❌ Нет бутылок")


@router.message(F.text.startswith("обмен"))
async def ex(msg):
    try:
        amount = int(msg.text.split()[1])
        res = exchange(msg.from_user.id, amount)

        if res is None:
            return await msg.answer("❌ минимум 100 💰")
        if res is False:
            return await msg.answer("❌ нет денег")

        await msg.answer(f"💱 +{res} 🧴 бутылок")

    except:
        await msg.answer("❌ формат: обмен 200")
