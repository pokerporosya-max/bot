from aiogram import Router, F
from aiogram.types import Message
from db import add_user

router = Router()

@router.message(F.text == "/start")
async def start_cmd(message: Message):
    await add_user(message.from_user.id, message.from_user.username)

    await message.answer(
        "Привет 👋\n\nДобро пожаловать в игрового бота."
    )
