import asyncio

from handlers import register_handlers

from utils.database import db_helper

from __init__ import bot, dp


async def main():
    await db_helper.create_tables()

    register_handlers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())