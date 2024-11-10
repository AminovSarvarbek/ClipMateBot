import os
from aiogram import F
from aiogram.types import Message, InputFile, FSInputFile
from loader import dp, bot
from utils.download import identify_and_download


@dp.message(F.text)
async def echo(message: Message):
    url = message.text
    await message.reply("Video yuklanmoqda  , iltimos kuting...")

    # Yuklab olish funksiyasini chaqiramiz
    video_path = await identify_and_download(url)

    # Xatolik yuz berganda yoki yuklanmaganda xabar chiqaramiz
    if video_path == "error":
        await message.reply("Video yuklashda xatolik yuz berdi yoki URL noto'g'ri.")
    elif video_path:
        try:
            video_file = FSInputFile(video_path)  # Fayl yo'lini FSInputFile orqali yuborish
            await bot.send_video(chat_id=message.chat.id, video=video_file)
        except Exception as e:
            await message.reply(f"Video yuborishda xatolik yuz berdi: {e}")
        finally:
            os.remove(video_path)
    else:
        await message.reply("Noma'lum xatolik yuz berdi.")