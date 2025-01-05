from aiogram import F
from aiogram.types import Message

from loader import dp
from models.user import User


@dp.message(F.text == '/start')
async def start_command(message: Message):
    try:
        user = await User.get(chat_id=chat_id)
    except Exception as e :
        user = await User.create(
            chat_id=message.chat.id, 
            first_name=message.chat.first_name
        )

    # send welcom
    await message.answer(
            f"👋 Salom, <b>{message.chat.first_name}</b>!\n"
            "🌟 Yuklovchi botga xush kelibsiz!\n\n"
            "📥 Menga <b>YouTube</b> yoki <b>Instagram</b> linklarini jo'nating, "
            "men esa sizga video yoki audio formatda jo'nataman. 😊",
            parse_mode="HTML"
        )