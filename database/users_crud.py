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


async def get_user_data(user_id: int = None, name: str = None, username: str = None):

    filters = {}
    if user_id is not None:
        filters["id"] = user_id
    if name is not None:
        filters["name"] = name
    if username is not None:
        filters["username"] = username

    return await User.get_or_none(**filters)
