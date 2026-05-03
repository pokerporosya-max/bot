from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from db import add_user

router = Router()

@router.message(F.text.startswith("/start"))
async def start(message: Message):

    await add_user(
        message.from_user.id,
        message.from_user.username
    )

    # кнопка в группу (инлайн)
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Добавить бота в чат",
                url="https://t.me/GachyxBot?startgroup=true"
            )
        ]
    ])

    # 🔥 ВОЗВРАЩАЕМ ТВОЁ МЕНЮ (как было)
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Профиль"), KeyboardButton(text="🎁 Бонус")],
            [KeyboardButton(text="🛒 Магазин"), KeyboardButton(text="🎮 Игры")],
            [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="ℹ️ О нас")],
            [KeyboardButton(text="💖 Поддержать"), KeyboardButton(text="📄 Соглашение")]
        ],
        resize_keyboard=True
    )

    # приветствие
    await message.answer(
        "👋 Привет!\n\n"
        "Добро пожаловать в игрового бота 🍬\n"
        "Играй, зарабатывай и попадай в топ 🏆\n\n"
        "Добавь бота в группу 👇",
        reply_markup=inline_kb
    )

    # меню (КАК У ТЕБЯ БЫЛО)
    await message.answer(
        "👇 Меню бота",
        reply_markup=menu
    )
