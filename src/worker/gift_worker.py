import asyncio
import aiohttp
import json
from database.models import Order
from database.orders_crud import get_all_orders, increment_completed_count
from database.users_crud import deduct_user_stars, get_user_data
from config import config
from logger import worker_logger
from helpers.fetch_gifts import fetch_gifts
from app import app
from user_bot import user_bot
from worker.errors import InsufficientStarsError


async def buy_gift_bot(gift, order: Order):

    if gift['price'] > order.user.stars:
        raise InsufficientStarsError("User does not have enough stars")

    await app.send_gift(
        chat_id=order.receiver_id,
        gift_id=gift['id']
    )
    if (await deduct_user_stars(
            order.user.id, gift['price'])):
        order = await increment_completed_count(order.id)
        order.user = await get_user_data(order.user.id)


async def buy_gift_userbot(gift, order: Order):
    await user_bot.send_gift(
        chat_id=order.receiver_id, gift_id=gift['id'])
    order = await increment_completed_count(order.id)


async def fulfill_orders(user_bot_id):

    orders = await get_all_orders()

    worker_logger.info(f"Found {len(orders)} orders to fulfill...")

    async with aiohttp.ClientSession() as session:

        gifts = await fetch_gifts(session)

        gifts = [gift for gift in gifts if gift["is_limited"]
                 and gift["available_amount"] > 0]

        if not gifts:
            worker_logger.info(
                "No gifts fetched, skipping order fulfillment.")
            return

        gifts.sort(key=lambda g: g["total_amount"])

        for order in orders:

            if order.completed_count >= order.count:
                continue

            worker_logger.info(
                f"Processing Order ID: {order.id}  for user {order.user.id}")

            for gift in gifts:

                if (not (order.min_stars <= gift["price"] <= order.max_stars and
                         order.min_supply <= gift["total_amount"] <= order.max_supply)):
                    continue

                needed = order.count - order.completed_count

                for i in range(needed):

                    worker_logger.info(
                        f"Gift ID: {gift['id']} → Receiver: {order.receiver_id} ")
                    try:
                        await buy_gift_bot(gift, order)
                    except Exception as e:
                        worker_logger.error(
                            f"Error sending gift {gift['id']} to {order.receiver_id} by BOT: {e}")

                        if (not user_bot_id or user_bot_id != order.user.id):
                            continue
                        try:
                            await buy_gift_userbot(gift, order)
                        except Exception as e:
                            worker_logger.error(
                                f"Error sending gift {gift['id']} to {order.receiver_id} by UserBOT: {e}")

                if order.completed_count >= order.count:
                    break
            else:
                worker_logger.info(
                    f"No suitable gift for order ID:{order.id}")


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
    worker_logger.info("Gift Worker started...")

    while True:
        try:
            await fulfill_orders(user_bot_id)
        except Exception as e:
            worker_logger.exception(f"Worker error: {e}")
            break
        await asyncio.sleep(config.CHECK_GIFT_INTERVAL)
