from typing import List
from .models import User
from .users_crud import get_user


async def list_channels(owner_id: int) -> List[User]:
    user = await User.get(id=owner_id)
    return list(await user.channels.all())


async def add_channel(owner_id: int, channel_identifier: str):
    user = await get_user(owner_id)
    channel = await get_user(channel_identifier)
    if not channel:
        return False, "not_found"

    channels = await user.channels.all()
    if len(channels) >= 3:
        return False, "limit"

    if (channel in channels):
        return False, "exists"

    await user.channels.add(channel)
    return True, str(channel.id)


async def remove_channel(owner_id: int, channel_identifier: str):
    user = await get_user(owner_id)
    channel = await get_user(channel_identifier)
    if not channel:
        return False, "not_found"
    deleted = await user.channels.remove(channel)
    return True, str(channel.id)
