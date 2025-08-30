from .models import User
from tortoise.expressions import F
from constants.roles import Roles
from .models import User
from typing import Optional, Tuple


async def _normalize_identifier(identifier: str) -> Tuple[Optional[int], Optional[str]]:

    try:
        return int(identifier), None
    except ValueError:
        pass
    ident = identifier.strip()
    uname = ident[1:] if ident.startswith("@") else ident
    uname = uname.strip()
    return None, uname.lower() if uname else None


async def get_user(identifier: str) -> Optional[User]:

    user_id, uname = await _normalize_identifier(identifier)
    if user_id is not None:
        return await User.get_or_none(id=user_id)
    if uname:
        return await User.get_or_none(username__iexact=uname)
    return None


async def add_user(user_id: int, role: str = Roles.RECEIVER.value, name: str = "none", username: str = "none") -> User:
    user = await User.create(id=user_id, name=name, username=username, role=role)
    return user


async def remove_user(identifier: str):
    user = await get_user(identifier)
    if user:
        await user.delete()
        return True
    return False


async def update_role(identifier: str, new_role: str):
    user = await get_user(identifier)
    if user:
        user.role = new_role
        await user.save()
        return True
    return False


async def add_user_stars(user_id: int, stars_amount: int) -> bool:
    updated_count = await User.filter(id=user_id).update(stars=F("stars") + stars_amount)
    return updated_count > 0


async def count_users() -> int:
    return await User.all().count()


async def get_users(page: int = 0, limit: int = 10):
    offset = page * limit
    return await User.all().offset(offset).limit(limit)


async def update_user_data(user_id: int, name: str, username: str):
    user = await get_user(user_id)
    if user:
        user.name = name
        user.username = username
        await user.save()
        return True
    return False


async def deduct_user_stars(user_id: int, stars_amount: int) -> bool:
    user = await get_user(user_id)
    if not user or user.stars < stars_amount:
        return False

    await User.filter(id=user_id).update(stars=F("stars") - stars_amount)
    return True
