import asyncio
from pyrogram import Client
from config import config
from logger import logger
import os

os.makedirs("sessions/user", exist_ok=True)


async def main():
    user = Client(
        "user_bot",
        api_id=int(config.API_ID),
        api_hash=config.API_HASH,
        workdir="sessions/user"
    )
    await user.start()
    logger.info("Logged in. Session saved.")
    await user.stop()

asyncio.run(main())
