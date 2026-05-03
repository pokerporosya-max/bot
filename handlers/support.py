from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(F.text.lower().contains("поддерж"))
async def support(message: Message):

    if message.chat.type != "private":
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ Поддержать через Stars", url="https://t.me/")],
        [InlineKeyboardButton(text="💎 Поддержать криптой", callback_data="support_crypto")]
    ])

    await message.answer(
        "💖 Поддержка проекта\n\n"
        "Если тебе нравится бот — ты можешь поддержать развитие проекта.\n\n"
        "⭐ Через Telegram Stars\n"
        "💎 Через криптовалюту (TON / USDT)\n\n"
        "Спасибо за поддержку ❤️",
        reply_markup=kb
    )


@router.callback_query(F.data == "support_crypto")
async def crypto(callback):
    await callback.message.answer(
        "💎 Крипто-поддержка\n\n"
        "TON: (UQDtjq8x5gsJj9l7igpYa_KBr7ULS7xlJ0moCpFZXV1Fwcxp)\n"
        "USDT: (UQDtjq8x5gsJj9l7igpYa_KBr7ULS7xlJ0moCpFZXV1Fwcxp)\n\n"
        "Спасибо ❤️"
    )
    await callback.answer()
