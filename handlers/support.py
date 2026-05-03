from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    LabeledPrice
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()

# ---------------------------
# FSM для Stars
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
        [InlineKeyboardButton(text="⭐ Поддержать Stars", callback_data="donate_stars")],
        [InlineKeyboardButton(text="💎 Крипта", callback_data="donate_crypto")]
    ])

    await message.answer(
        "💖 Поддержка проекта\n\n"
        "Выбери способ поддержки:",
        reply_markup=kb
    )

# ---------------------------
# STARS: ввод суммы
# ---------------------------
@router.callback_query(F.data == "donate_stars")
async def stars_start(callback: CallbackQuery, state: FSMContext):

    await callback.message.answer(
        "⭐ Введите сумму в Stars\n\n"
        "Пример: 50 / 100 / 500\n"
        "Минимум: 1 ⭐"
    )

    await DonateState.amount.set()
    await callback.answer()

# ---------------------------
# STARS: обработка суммы
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
        title="💖 Поддержка проекта",
        description=f"Спасибо за {amount}⭐",
        payload="donate_support",
        provider_token="",
        currency="XTR",
        prices=prices
    )

# ---------------------------
# КРИПТА
# ---------------------------
@router.callback_query(F.data == "donate_crypto")
async def crypto(callback: CallbackQuery):

    await callback.message.answer(
        "💎 Крипто-поддержка\n\n"
        "TON: <UQDtjq8x5gsJj9l7igpYa_KBr7ULS7xlJ0moCpFZXV1Fwcxp>\n"
        "USDT (TRC20): <UQDtjq8x5gsJj9l7igpYa_KBr7ULS7xlJ0moCpFZXV1Fwcxp>\n\n"
        "Спасибо за поддержку ❤️"
    )

    await callback.answer()

# ---------------------------
# УСПЕШНАЯ ОПЛАТА STARS
# ---------------------------
@router.message(F.successful_payment)
async def success_payment(message: Message):

    amount = message.successful_payment.total_amount

    await message.answer(
        "💖 Спасибо за поддержку!\n\n"
        f"Ты отправил: {amount}⭐\n"
        "Ты реально помогаешь развитию бота ❤️"
    )
