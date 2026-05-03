from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.lower() == "ℹ️ о нас")
async def about(message: Message):

    # только личка
    if message.chat.type != "private":
        return

    await message.answer(
        "ℹ️ О нас\n\n"
        "Этот бот — игровая экономическая система.\n\n"
        "🎮 Играй в мини-игры\n"
        "💰 Зарабатывай конфеты 🍬\n"
        "🌵 Выращивай кактус\n"
        "🏆 Соревнуйся с другими игроками\n\n"
        "Бот создан для развлечения и соревнования между пользователями."
    )
