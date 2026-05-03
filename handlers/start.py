from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from db import add_user

router = Router()

@router.message(lambda m: m.text == "/start")
async def start_cmd(message: Message):
    await add_user(message.from_user.id, message.from_user.username)

    # инлайн кнопка (добавить в группу)
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить бота в чат", url="https://t.me/GachyxBot?startgroup=true")]
    ])

    # меню клавиатура
    menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Профиль"), KeyboardButton(text="🎁 Бонус")],
            [KeyboardButton(text="🛒 Магазин"), KeyboardButton(text="🎮 Игры")],
            [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="ℹ️ О нас")],
            [KeyboardButton(text="💖 Поддержать"), KeyboardButton(text="📄 Соглашение")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "Привет 👋\n\nДобро пожаловать в игрового бота.\n\nДобавь бота в чат, чтобы начать игру вместе с друзьями.",
        reply_markup=inline_kb
    )

    # открываем меню
    await message.answer(
        "👇 Меню бота",
        reply_markup=menu
    )
