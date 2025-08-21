import asyncio
import nest_asyncio
from pyrogram import idle
from app import app, init_handlers
from database import init_db
from worker.gift_worker import gift_worker_loop
from logger import logger
from user_bot import user_bot
import os

nest_asyncio.apply()


async def userbot_loop():
    if (os.path.exists("sessions/user")):
        await user_bot.start()
        await idle()
        await user_bot.stop()


async def bot_loop():
    await init_db()
    init_handlers(app)
    await app.start()
    logger.info("🤖 Bot is running...")
    await idle()

    await app.stop()


async def main():
    await asyncio.gather(
        userbot_loop(),
        bot_loop(),
        gift_worker_loop(),
    )


if __name__ == "__main__":
    asyncio.run(main())
