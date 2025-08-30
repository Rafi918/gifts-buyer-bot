import aiohttp
import tempfile
import os
from config import config
from logger import logger
from database.models import User
from database.users_crud import get_users
from constants.roles import Roles
from pyrogram import Client
import json
from pathlib import Path

NOTIFIED_FILE = Path("data/notified_gifts.json")


def load_notified() -> dict:
    if NOTIFIED_FILE.exists():
        with open(NOTIFIED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_notified(data: dict):
    with open(NOTIFIED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


async def notify_new_gift(client: Client, chat_id: int, gift: dict):

    notified = load_notified()
    gift_id = str(gift["id"])
    chat_key = str(chat_id)

    if chat_key not in notified:
        notified[chat_key] = []

    if gift_id in notified[chat_key] and not gift.get("test", False):
        logger.info(f"Gift {gift_id} already notified, skipping.")
        return

    url = f"{config.API_URL}/gift/{gift['sticker']['file_unique_id']}"

    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".tgs")
    os.close(tmp_fd)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"Failed to fetch gift: {resp.status}")
                with open(tmp_path, "wb") as f:
                    f.write(await resp.read())

        sticker_msg = await client.send_sticker(chat_id=chat_id, sticker=tmp_path)
        await sticker_msg.reply_text(text="`{}` \n \n**💎 Price: ** {}⭐️\n**🎯 Total amount: ** {} \n ^_^".format(gift['id'], gift['price'], gift['total_amount']), quote=True)

        notified[chat_key].append(gift_id)
        save_notified(notified)

    except Exception as e:
        logger.error(f"Error notifying new gift: {e}")

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


async def notify_users(client, gift: dict):
    users = await get_users()
    for user in users:
        if (user.role != Roles.RECEIVER.value):
            await notify_new_gift(client, user.id, gift)


async def notify_test_gift(client, chat_id: int):

    test_gifts = [
        {
            "id": "5170233102089322756",
            "sticker": {
                "file_unique_id": "AgADrVQAApo_6Uo"
            },
            "price": 15,
            "total_amount": "∞",
            "test": True
        },
        {
            "id": "5170145012310081615",
            "sticker": {
                "file_unique_id": "AgADfBsAApKE2Es"
            },
            "price": 15,
            "total_amount": "∞",
            "test": True
        }
    ]

    for gift in test_gifts:
        await notify_new_gift(client, chat_id, gift)
