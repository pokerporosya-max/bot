from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from db import update_balance

router = Router()

# ---------------------------
# МАГАЗИН
# ---------------------------
@router.message(F.text.lower().contains("магазин"))
async def shop(message: Message):

    if message.chat.type != "private":
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍬 500 конфет — 15⭐", callback_data="buy_500")],
        [InlineKeyboardButton(text="🍬 1000 конфет — 30⭐", callback_data="buy_1000")],
        [InlineKeyboardButton(text="🍬 2500 конфет — 70⭐", callback_data="buy_2500")],
        [InlineKeyboardButton(text="🍬 5000 конфет — 130⭐", callback_data="buy_5000")],
        [InlineKeyboardButton(text="🍬 10000 конфет — 250⭐", callback_data="buy_10000")]
    ])

    await message.answer(
        "🛒 Магазин конфет\n\n"
        "Выбери пакет и оплати через ⭐ Stars:",
        reply_markup=kb
    )

# ---------------------------
# ТОВАРЫ
# ---------------------------
PACKS = {
    "buy_500": (500, 15),
    "buy_1000": (1000, 30),
    "buy_2500": (2500, 70),
    "buy_5000": (5000, 130),
    "buy_10000": (10000, 250),
}

# ---------------------------
# ПОКУПКА
# ---------------------------
@router.callback_query(F.data.startswith("buy_"))
async def buy(callback: CallbackQuery):

    item = PACKS.get(callback.data)

    if not item:
        return await callback.answer("❌ Товар не найден")

    candies, stars = item

    prices = [LabeledPrice(label=f"{candies} конфет", amount=stars)]

    await callback.message.bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="🛒 Покупка конфет",
        description=f"{candies} конфет за {stars}⭐",
        payload=f"buy_{candies}",
        provider_token="",
        currency="XTR",
        prices=prices
    )

    await callback.answer()

# ---------------------------
# ОПЛАТА УСПЕШНА
# ---------------------------
@router.message(F.successful_payment)
async def success_payment(message: Message):

    payload = message.successful_payment.invoice_payload

    if payload.startswith("buy_"):
        candies = int(payload.split("_")[1])

        await update_balance(message.from_user.id, candies)

        await message.answer(
            "🍬 Покупка успешна!\n\n"
            f"Ты получил +{candies} конфет!"
  )
