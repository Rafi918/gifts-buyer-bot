import asyncio
import aiohttp
import json
import logging
from database.orders_crud import get_all_orders, increment_completed_count
from database.users_crud import deduct_user_stars
from config import config
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("gift_worker")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/gift_worker.log")
file_handler.setLevel(logging.INFO)


async def fetch_gifts(session):
    async with session.get("https://buygifts.vercel.app/") as resp:
        resp.raise_for_status()
        text = await resp.text()
        return json.loads(text)["available gifts"]


async def fulfill_orders(app):

    orders = await get_all_orders()

    logging.info(f"Found {len(orders)} orders to fulfill...")

    async with aiohttp.ClientSession() as session:
        gifts = await fetch_gifts(session)
        gifts.sort(key=lambda g: g["price"], reverse=True)

        for order in orders:

            if order.completed_count >= order.count:
                continue

            logging.info(f"Processing Order ID: {order.id} ")

            for gift in gifts:
                if not gift["is_limited"]:
                    continue

                if gift["price"] > order.user.stars or gift["available_amount"] == 0:
                    continue

                if (order.min_stars <= gift["price"] <= order.max_stars and
                        order.min_supply <= gift["total_amount"] <= order.max_supply):

                    needed = order.count - order.completed_count

                    for i in range(needed):
                        if (gift['price'] > order.user.stars):
                            break
                        logging.info(
                            f"Gift ID: {gift['id']} → Receiver: {order.receiver_id} ")
                        try:
                            await app.send_gift(
                                chat_id=order.receiver_id,
                                gift_id=gift['id']
                            )
                            await increment_completed_count(order.id)
                            await deduct_user_stars(
                                order.user.id, gift['price'])

                        except Exception as e:
                            logging.error(
                                f"Error sending gift {gift['id']} to {order.receiver_id}: {e}")

                if order.completed_count >= order.count:
                    break
            else:
                logging.info(
                    f"No suitable gift for order  `{order.id}`")


async def gift_worker_loop(app):
    logging.info("Gift Worker started...")
    while True:
        try:
            await fulfill_orders(app)
        except Exception as e:
            logging.exception(f"Worker error: {e}")
            break
        await asyncio.sleep(config.CHECK_GIFT_INTERVAL)
