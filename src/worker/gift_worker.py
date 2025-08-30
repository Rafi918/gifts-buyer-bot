import asyncio
import aiohttp
from database.orders_crud import get_all_orders
from helpers.fetch_gifts import fetch_gifts
from helpers.notify_gift import notify_users
from helpers.buy_gift import try_buying_gift
from app import app
from user_bot import user_bot
from config import config
from logger import worker_logger


async def fulfill_orders(user_bot_id):

    orders = await get_all_orders()

    worker_logger.info(f"Found {len(orders)} orders to fulfill...")

    async with aiohttp.ClientSession() as session:

        gifts = await fetch_gifts(session)

        gifts = [gift for gift in gifts if gift["is_limited"]
                 and gift["available_amount"] > 0]

        gifts.sort(key=lambda g: g["total_amount"])

        for gift in gifts:
            await notify_users(app, gift)

        if not gifts:
            worker_logger.info("No gifts fetched, skipping order fulfillment.")
            return

        for order in orders:

            if order.completed_count >= order.count or gift['price'] == -1:
                continue

            worker_logger.info(
                f"Processing Order ID: {order.id}  for user {order.user.id}")

            for gift in gifts:

                if (not (order.min_stars <= gift["price"] <= order.max_stars and
                         order.min_supply <= gift["total_amount"] <= order.max_supply)):
                    continue

                needed = order.count - order.completed_count

                for i in range(needed):
                    await try_buying_gift(app, user_bot, gift, order, user_bot_id)

                if order.completed_count >= order.count:
                    break
            else:
                worker_logger.info(f"No suitable gift for order ID:{order.id}")


async def wait_for_clients():
    for attempt in range(5):
        try:
            user_bot_data = await user_bot.get_me()
            await app.get_me()

            return user_bot_data.id

        except Exception as e:
            worker_logger.error(f"Can't connect to UserBOT: {e}")
            await asyncio.sleep(5)

    return None


async def gift_worker_loop():

    user_bot_id = await wait_for_clients()
    if (user_bot_id):
        worker_logger.info(
            f"Gift Worker Bot and UserBOT {user_bot_id} started...")
    else:
        worker_logger.info("Gift Worker Bot started...")

    while True:
        try:
            await fulfill_orders(user_bot_id)
        except Exception as e:
            worker_logger.exception(f"Worker error: {e}")
            break
        await asyncio.sleep(config.CHECK_GIFT_INTERVAL)
