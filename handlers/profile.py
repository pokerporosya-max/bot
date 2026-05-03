from aiogram import Router, F
from db import get_user, create_user
from keyboards import menu

router = Router()


@router.message(F.text == "👤 Профиль")
async def profile(msg):
    create_user(msg.from_user.id)
    u = get_user(msg.from_user.id)

    await msg.answer(
        f"""👤 Профиль

💰 Баланс: {u[1]}
🧴 Бутылки: {u[2]}

📊 Рекорд: {u[7]} 💥
🌵 Кактус: {u[3]} см
🧴 Фап: {u[4]}

🎲 Игр: {u[5]} | 🏆 Побед: {u[5]} | ❌ Поражений: {u[6]}""",
        reply_markup=menu
    )
