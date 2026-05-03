from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()

# ---------------------------
# STATE
# ---------------------------
class DonateState(StatesGroup):
    amount = State()

# ---------------------------
# МЕНЮ ПОДДЕРЖКИ
# ---------------------------
@router.message(F.text.lower().contains("поддерж"))
async def support(message: Message):

    if message.chat.type != "private":
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ Stars", callback_data="donate_stars")],
        [InlineKeyboardButton(text="💎 TON / USDT", callback_data="donate_crypto")]
    ])

    await message.answer(
        "💖 Поддержка проекта\n\n"
        "Выбери способ поддержки:",
        reply_markup=kb
    )

# ---------------------------
# STARS START
# ---------------------------
@router.callback_query(F.data == "donate_stars")
async def stars_start(callback: CallbackQuery, state: FSMContext):

    await callback.message.answer(
        "⭐ Введите сумму в Stars\n\n"
        "Пример: 50 / 100 / 500"
    )

    await state.set_state(DonateState.amount)
    await callback.answer()

# ---------------------------
# STARS AMOUNT
# ---------------------------
@router.message(DonateState.amount)
async def stars_amount(message: Message, state: FSMContext):

    if not message.text.isdigit():
        return await message.answer("❌ Введите число")

    amount = int(message.text)

    if amount < 1:
        return await message.answer("❌ Минимум 1 ⭐")

    await state.clear()

    prices = [LabeledPrice(label="Support", amount=amount)]

    await message.bot.send_invoice(
        chat_id=message.chat.id,
        title="💖 Поддержка",
        description=f"Спасибо за {amount}⭐",
        payload="donate_support",
        provider_token="",
        currency="XTR",
        prices=prices
    )

# ---------------------------
# CRYPTO
# ---------------------------
@router.callback_query(F.data == "donate_crypto")
async def crypto(callback: CallbackQuery):

    wallet = "UQDtjq8x5gsJj9l7igpYa_KBr7ULS7xlJ0moCpFZXV1Fwcxp"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Скопировать адрес", url=f"tg://msg?text={wallet}")]
    ])

    await callback.message.answer(
        "💎 Поддержка криптой\n\n"
        f"TON / USDT (один адрес):\n`{wallet}`\n\n"
        "Нажми кнопку чтобы скопировать 👇",
        reply_markup=kb,
        parse_mode="Markdown"
    )

    await callback.answer()

# ---------------------------
# SUCCESS PAYMENT
# ---------------------------
@router.message(F.successful_payment)
async def success_payment(message: Message):

    amount = message.successful_payment.total_amount

    await message.answer(
        "💖 Спасибо за поддержку ❤️\n\n"
        f"Ты отправил: {amount}⭐"
    )
