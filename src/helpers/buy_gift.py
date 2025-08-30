
from database.models import Order
from database.orders_crud import increment_completed_count
from database.users_crud import deduct_user_stars, get_user
from logger import worker_logger
from helpers.errors import InsufficientStarsError
from pyrogram import Client


async def buy_gift_bot(client: Client, gift, order: Order):

    if gift['price'] > order.user.stars:
        raise InsufficientStarsError("User does not have enough stars")

    await client.send_gift(
        chat_id=order.receiver_id,
        gift_id=gift['id'],
        is_private=True,
    )
    if (await deduct_user_stars(
            order.user.id, gift['price'])):
        order = await increment_completed_count(order.id)
        order.user = await get_user(order.user.id)
        return order


async def buy_gift_userbot(client: Client, gift, order: Order):
    await client.send_gift(
        chat_id=order.receiver_id, gift_id=gift['id'], is_private=True)
    return await increment_completed_count(order.id)


async def try_buying_gift(app: Client, user_bot: Client, gift, order: Order, user_bot_id):
    try:
        if (order.completed_count >= order.count):
            return order

        return await buy_gift_bot(app, gift, order)
    except Exception as e:
        worker_logger.error(
            f"Error sending gift {gift['id']} to {order.receiver_id} by BOT: {e}")

        if (not user_bot_id or user_bot_id != order.user.id):
            return
        try:
            return await buy_gift_userbot(user_bot, gift, order)
        except Exception as e:
            worker_logger.error(
                f"Error sending gift {gift['id']} to {order.receiver_id} by UserBOT: {e}")
