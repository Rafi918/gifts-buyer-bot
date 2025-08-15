import asyncio
import aiohttp
import json
from database.orders_crud import get_all_orders, increment_completed_count
from database.users_crud import deduct_user_stars, get_user_data
from config import config
from logger import worker_logger
from helpers.fetch_gifts import fetch_gifts


async def fulfill_orders(app, user_bot):

    user_stars_in_account = await user_bot.get_stars_balance()
    orders = await get_all_orders()

    worker_logger.info(f"Found {len(orders)} orders to fulfill...")

    async with aiohttp.ClientSession() as session:
        gifts = await fetch_gifts(session)

        gifts = [gift for gift in gifts if gift["is_limited"]
                 and gift["available_amount"] > 0]

        if not gifts:
            worker_logger.error(
                "No gifts fetched, skipping order fulfillment.")
            return

        gifts.sort(key=lambda g: g["price"], reverse=True)
        for order in orders:

            if order.completed_count >= order.count:
                continue

            worker_logger.info(
                f"Processing Order ID: {order.id}  for user {order.user.id}")

            for gift in gifts:

                if gift["price"] > order.user.stars:
                    continue

                if (order.min_stars <= gift["price"] <= order.max_stars and
                        order.min_supply <= gift["total_amount"] <= order.max_supply):

                    needed = order.count - order.completed_count

                    for i in range(needed):
                        if gift['price'] > order.user.stars:
                            break
                        worker_logger.info(
                            f"Gift ID: {gift['id']} → Receiver: {order.receiver_id} ")
                        try:

                            await app.send_gift(
                                chat_id=order.receiver_id,
                                gift_id=gift['id']
                            )
                            if (await deduct_user_stars(
                                    order.user.id, gift['price'])):
                                order = await increment_completed_count(order.id)
                                order.user = await get_user_data(order.user.id)

                        except Exception as e:
                            worker_logger.error(
                                f"Error sending gift {gift['id']} to {order.receiver_id}: {e}")

                if order.completed_count >= order.count:
                    break
            else:
                worker_logger.info(
                    f"No suitable gift for order ID:{order.id}")




async def gift_worker_loop(app):
    worker_logger.info("Gift Worker started...")
    while True:
        try:
            await fulfill_orders(app)
        except Exception as e:
            worker_logger.exception(f"Worker error: {e}")
            break
        await asyncio.sleep(config.CHECK_GIFT_INTERVAL)
