import os
import asyncio
import uuid
from aiogram import F, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from utils.download import identify_and_download
import moviepy as mp
from loader import bot, dp
import shutil

# Yuklash cheklovini boshqarish uchun semaphore
semaphore = asyncio.Semaphore(10)

# Foydalanuvchi vaqtinchalik katalog yaratish
def create_temp_dir(chat_id):
    temp_dir = f"temp/{chat_id}"
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

# Fayllarni tozalash
def cleanup_temp_dir(temp_dir):
    shutil.rmtree(temp_dir, ignore_errors=True)

# Tugmalar
video_audio_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🎥 Video", callback_data="send_video"),
            InlineKeyboardButton(text="🔊 Audio", callback_data="send_audio"),
        ]
    ]
)

bot_link_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="🤖 Botga o'tish", url="https://t.me/ClipMateRobot")]]
)

# Xabar metadatalarini saqlash
message_metadata = {}

# Video va audio yaratish funksiyasi
async def download_video_and_audio(video_path, temp_dir):
    audio_path = os.path.join(temp_dir, f"{uuid.uuid4()}.mp3")
    await asyncio.to_thread(
        lambda: mp.VideoFileClip(video_path).audio.write_audiofile(audio_path)
    )
    return video_path, audio_path

# Xabarlarni boshqarish
@dp.message(F.text)
async def handle_message(message: Message):
    url = message.text.strip()
    temp_message = await message.reply("⏳ Video yuklanmoqda, iltimos kuting...")
    chat_id = message.chat.id
    temp_dir = create_temp_dir(chat_id)

    try:
        async with semaphore:
            # Video yuklash
            video_path = await identify_and_download(url)
            if video_path == "error" or not video_path:
                await message.reply("❌ Video yuklashda xatolik yuz berdi yoki URL noto'g'ri.")
                return

            # Faylni vaqtinchalik katalogga ko'chirish
            video_filename = os.path.basename(video_path)
            temp_video_path = os.path.join(temp_dir, video_filename)
            shutil.move(video_path, temp_video_path)

        # Inline tugmalar bilan javob
        select_message = await message.reply(
            "✅ Video yuklandi! Iltimos, kerakli formatni tanlang:", reply_markup=video_audio_buttons
        )
        message_metadata[chat_id] = {
            "select_message_id": select_message.message_id,
            "video_path": temp_video_path,
            "temp_dir": temp_dir
        }

    except Exception as e:
        await message.reply(f"⚠️ Yuklashda xatolik yuz berdi: {e}")
    finally:
        await bot.delete_message(chat_id=chat_id, message_id=temp_message.message_id)

# Callbacklar uchun handler
@dp.callback_query(F.data.in_({"send_video", "send_audio"}))
async def handle_callback_query(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    metadata = message_metadata.get(chat_id)

    if not metadata:
        await callback_query.answer("⚠️ Ma'lumot topilmadi. Iltimos, qayta urinib ko'ring.")
        return

    video_path = metadata["video_path"]
    temp_dir = metadata["temp_dir"]
    description = "🎬 Yuklangan video/audio! Marhamat, zavqlaning! 🎶"

    try:
        # Tugmalarni o'chirish
        if metadata.get("select_message_id"):
            try:
                await bot.delete_message(chat_id=chat_id, message_id=metadata["select_message_id"])
            except Exception:
                pass  # Agar xabar allaqachon o'chirilgan bo'lsa, xatolikni e'tiborsiz qoldirish

        # Asinxron yuklash va jo'natish
        if callback_query.data == "send_video":
            await bot.send_video(
                chat_id=chat_id,
                video=FSInputFile(video_path),
                caption=description,
                reply_markup=bot_link_button,
            )
            await callback_query.answer("🎥 Video jo'natildi!")

        elif callback_query.data == "send_audio":
            audio_path = os.path.join(temp_dir, f"{uuid.uuid4()}.mp3")
            _, audio_path = await download_video_and_audio(video_path, temp_dir)
            await bot.send_audio(
                chat_id=chat_id,
                audio=FSInputFile(audio_path),
                caption=description,
                reply_markup=bot_link_button,
            )
            await callback_query.answer("🔊 Audio jo'natildi!")

    except Exception as e:
        await callback_query.message.reply(f"⚠️ Xatolik yuz berdi: {e}")
    finally:
        cleanup_temp_dir(temp_dir)
        message_metadata.pop(chat_id, None)
