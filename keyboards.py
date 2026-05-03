from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Профиль"), KeyboardButton(text="💰 Бонус")],
        [KeyboardButton(text="🎲 Кубик"), KeyboardButton(text="🌵 Полить")],
        [KeyboardButton(text="🧴 Фап"), KeyboardButton(text="💸 Перевод")],
        [KeyboardButton(text="🏆 Топ"), KeyboardButton(text="❓ Помощь")],
        [KeyboardButton(text="📜 Соглашение"), KeyboardButton(text="ℹ️ О нас")]
    ],
    resize_keyboard=True
)
