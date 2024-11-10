import asyncio
import logging
import sys
from config.data import BOT_TOKEN, DB_URL  # DB_URL baza manzili
from tortoise import Tortoise
from loader import dp, bot

import handlers


async def init_db() -> None:
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": ["models.user",]}  # Tortoise modeli uchun to‘g‘ri modul nomi
    )
    await Tortoise.generate_schemas()
# AgACAgQAAxkBAAOYZyebQSA7KOh6CR3-Sb6EDHhDkBsAAiO2MRuxk-xTWtos31RxWCUBAAMCAANzAAM2BA
# @dp.message()
# async def echo_for_getData(message):
#     print(message)

async def main() -> None:
    

    # Tortoise ORM ulanishi
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
