import asyncio
import nest_asyncio
from pyrogram import idle
from app import app, init_handlers
from database import init_db
from worker.gift_worker import gift_worker_loop
from logger import logger

nest_asyncio.apply()


async def bot_loop():
    await init_db()
    init_handlers(app)
    await app.start()
    logger.info("🤖 Bot is running...")
    await idle()
    await app.stop()


async def main():
    await asyncio.gather(
        bot_loop(),
        gift_worker_loop(app)
    )


if __name__ == "__main__":
    asyncio.run(main())
