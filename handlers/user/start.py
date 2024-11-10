from aiogram import F
from aiogram.types import Message
from loader import dp


@dp.message(F.text == '/start')
async def start_command(message: Message):
    await message.answer("Salom yuklovchi botga xush kelibsiz!\n\nMenga youtube, instagram dagi linklarni jo'nating")