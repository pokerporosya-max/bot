from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

router = Router()

# 🎮 Меню игр
@router.message(F.text == "🎮 Игры")
async def games_menu(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Кубик", callback_data="game_dice")]
    ])

    await message.answer(
        "🎮 Игры\n\n"
        "Выбери игру:",
        reply_markup=kb
    )

# 🎲 Описание кубика
@router.callback_query(F.data == "game_dice")
async def game_dice_info(callback: CallbackQuery):
    await callback.message.answer(
        "🎲 Кубик\n\n"
        "Как играть:\n"
        "— Сделай ставку: кубик <сумма>\n"
        "— Бот бросает кубик 🎲\n"
        "— Получаешь результат\n\n"
        "📊 Условия:\n"
        "4 и 6 — победа x2 🎉\n"
        "1, 2, 3, 5 — проигрыш 💀\n\n"
        "Все результаты идут в профиль"
    )

    await callback.answer()
