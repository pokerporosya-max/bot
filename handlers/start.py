from aiogram import Router
from aiogram.types import Message
from db import add_user

router = Router()

@router.message()
async def register_user(message: Message):
    await add_user(message.from_user.id, message.from_user.username)
