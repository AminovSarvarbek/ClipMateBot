import asyncio
import logging
import sys
from config.data import BOT_TOKEN, DB_URL
from tortoise import Tortoise
from loader import dp, bot

import handlers


async def init_db() -> None:
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": ["models.user",]}  # Tortoise modeli uchun to‘g‘ri modul nomi
    )
    await Tortoise.generate_schemas()


async def main() -> None:
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
