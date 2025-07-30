from .models import User


async def add_user(user_id: int, role: str = "receiver", name: str = "none", username: str = "none") -> User:
    user = await User.create(id=user_id, name=name, username=username, role=role)
    return user


async def remove_user(user_id: int):
    user = await User.get_or_none(id=user_id)
    if user:
        await user.delete()
        return True
    return False


async def add_user_stars(user_id: int, stars_amount: int) -> bool:
    user = await User.get_or_none(id=user_id)
    if not user:
        return False
    user.stars += stars_amount
    await user.save()
    return True


async def remove_user_stars(user_id: int, stars_amount: int) -> bool:
    user = await User.get_or_none(id=user_id)
    if not user:
        return False
    if user.stars >= stars_amount:
        user.stars -= stars_amount
        await user.save()
        return True

    return False


async def get_user_data(user_id: int):
    return await User.get_or_none(id=user_id)


async def count_users() -> int:
    return await User.all().count()


async def get_users(page: int = 0, limit: int = 10):
    offset = page * limit
    return await User.all().offset(offset).limit(limit)


async def update_role(user_id: int, new_role: str):
    user = await User.get_or_none(id=user_id)
    if user:
        user.role = new_role
        await user.save()
        return True
    return False
