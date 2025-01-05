from aiogram.filters import BaseFilter
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot

class SubscribeFilter(BaseFilter):
    def __init__(self, channels: list):
        self.channels = channels

    async def __call__(self, message: Message, bot: Bot) -> bool:
        subscription_buttons = []
        user_id = message.from_user.id

        for channel_id in self.channels:
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                # Kanalga obuna bo'lish uchun tugma yaratish
                subscription_buttons.append(
                    [
                        InlineKeyboardButton(
                            text="📢 Kanalga obuna bo‘lish",
                            url=f"https://t.me/{(await bot.get_chat(chat_id=channel_id)).username}"
                        )
                    ]
                )

        if subscription_buttons:
            await message.reply(
                "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘lishingiz kerak:",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=subscription_buttons),
            )
            return False

        return True
