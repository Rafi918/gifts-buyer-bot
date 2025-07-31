from .models import Order
from tortoise.expressions import F

async def add_order(user_id, min_stars, max_stars, min_supply, max_supply, count, receiver_id):
    return await Order.create(
        user_id=user_id,
        min_stars=min_stars,
        max_stars=max_stars,
        min_supply=min_supply,
        max_supply=max_supply,
        count=count,
        receiver_id=receiver_id
    )


async def get_all_orders():
    return await Order.filter().all().prefetch_related("user", "receiver")


async def get_orders(user_id):
    return await Order.filter(user_id=user_id).all().prefetch_related("user", "receiver")


async def remove_order(user_id, order_id):
    await Order.filter(id=order_id, user_id=user_id).delete()


async def increment_completed_count(order_id: int):
    await Order.filter(id=order_id).update(completed_count=F("completed_count") + 1)
