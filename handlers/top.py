from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from db import top_balance, top_games, top_cactus

router = Router()

# 📊 Топ меню (любая раскладка)
@router.message(F.text.lower() == "топ")
async def top_menu(message: Message):

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Баланс", callback_data="top_balance")],
        [InlineKeyboardButton(text="🎮 Игры", callback_data="top_games")],
        [InlineKeyboardButton(text="🌵 Кактус", callback_data="top_cactus")]
    ])

    await message.answer("📊 Выбери топ:", reply_markup=kb)

# 💰 ТОП БАЛАНС
@router.callback_query(F.data == "top_balance")
async def balance_top(callback: CallbackQuery):

    data = await top_balance()

    text = "💰 ТОП БАЛАНС\n\n"
    for i, u in enumerate(data, 1):
        text += f"{i}. {u['username']} — {u['balance']} 🍬\n"

    await callback.message.answer(text)
    await callback.answer()

# 🎮 ТОП ИГР
@router.callback_query(F.data == "top_games")
async def games_top(callback: CallbackQuery):

    data = await top_games()

    text = "🎮 ТОП ИГР\n\n"
    for i, u in enumerate(data, 1):
        text += f"{i}. {u['username']} — {u['games']}\n"

    await callback.message.answer(text)
    await callback.answer()

# 🌵 ТОП КАКТУС
@router.callback_query(F.data == "top_cactus")
async def cactus_top(callback: CallbackQuery):

    data = await top_cactus()

    text = "🌵 ТОП КАКТУС\n\n"
    for i, u in enumerate(data, 1):
        text += f"{i}. {u['username']} — {u['cactus']} см\n"

    await callback.message.answer(text)
    await callback.answer()
