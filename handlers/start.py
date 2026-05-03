from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from db import add_user

router = Router()

@router.message(F.text.lower().in_({"/start", "start"}))
async def start(message: Message):

    # добавляем пользователя в БД
    await add_user(
        message.from_user.id,
        message.from_user.username
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Добавить бота в группу",
                url="https://t.me/GachyxBot?startgroup=true"
            )
        ]
    ])

    await message.answer(
        "👋 Привет!\n\n"
        "Добро пожаловать в игровой бот 🍬\n"
        "Зарабатывай конфеты, играй и поднимайся в топ 🏆\n\n"
        "Добавь бота в группу, чтобы играть с друзьями 👇",
        reply_markup=kb
    )
