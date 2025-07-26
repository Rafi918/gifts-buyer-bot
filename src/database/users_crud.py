from models import User


async def add_user(user_id: int, name: str, username: str, role: str) -> User:
    user = await User.create(id=user_id, name=name, username=username, role=role)
    return user


async def update_user_stars(user_id: int, stars: int) -> bool:
    user = await User.get_or_none(id=user_id)
    if not user:
        return False

    user.stars = stars
    await user.save()
    return True


async def get_user_data(user_id: int):
    return await User.get_or_none(id=user_id)

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
