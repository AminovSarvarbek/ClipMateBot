from aiogram import Bot, Dispatcher, html
from aiogram import Bot, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config.data import BOT_TOKEN, DB_URL, CHANNELS
from filters.subscribe_filter import SubscribeFilter


dp = Dispatcher()
dp.message.filter(SubscribeFilter(channels=CHANNELS))
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))