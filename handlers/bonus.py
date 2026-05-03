from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db import update_balance

router = Router()

@router.message(F.text == "🎁 Бонус")
async def bonus(message: Message):

    # если не ЛС — отправляем переход
    if message.chat.type != "private":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🚀 Перейти в бота",
                url="https://t.me/YOUR_BOT_USERNAME"
            )]
        ])

        return await message.answer(
            "🎁 Бонус\n\n"
            "Чтобы получить награду, перейди в личные сообщения с ботом.\n\n"
            "⚠️ Бонус можно получить только внутри бота",
            reply_markup=kb
        )

    # если ЛС — выдаём бонус
    await update_balance(message.from_user.id, 2500)

    await message.answer("🎁 Ты получил: 2500 🍬")
