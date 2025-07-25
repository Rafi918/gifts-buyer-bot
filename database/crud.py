from .models import Order

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

async def get_orders(user_id):
    return await Order.filter(user_id=user_id).all()

async def remove_order(user_id, order_id):
    await Order.filter(id=order_id, user_id=user_id).delete()
