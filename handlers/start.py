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

    # 🔗 кнопка добавления в группу
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Добавить бота в чат",
                url="https://t.me/GachyxBot?startgroup=true"
            )
        ]
    ])

    # 📱 главное меню
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Профиль"), KeyboardButton(text="🎁 Бонус")],
            [KeyboardButton(text="🛒 Магазин"), KeyboardButton(text="🎮 Игры")],
            [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="ℹ️ О нас")],
            [KeyboardButton(text="💖 Поддержать"), KeyboardButton(text="📄 Соглашение")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выбери действие 👇"
    )

    # 👋 приветствие
    await message.answer(
        "👋 <b>Привет!</b>\n\n"
        "Добро пожаловать в игрового бота 🍬\n"
        "Зарабатывай конфеты, играй и попадай в топ 🏆\n\n"
        "Добавь бота в группу, чтобы играть с друзьями 👇",
        reply_markup=inline_kb,
        parse_mode="HTML"
    )

    # 📋 меню
    await message.answer(
        "👇 <b>Меню бота</b>",
        reply_markup=menu,
        parse_mode="HTML"
    )
