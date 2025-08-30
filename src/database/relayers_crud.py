from typing import List
from .models import User
from .users_crud import get_user


async def list_relayers(owner_id: int) -> List[User]:
    user = await User.get(id=owner_id)
    return list(await user.relayers.all())


async def list_relay_targets(relayer_id: int) -> List[User]:

    relayer = await User.get(id=relayer_id)
    return list(await relayer.as_relayer_for.all())


async def add_relayer(owner_id: int, relayer_identifier: str):
    user = await get_user(owner_id)
    relayer = await get_user(relayer_identifier)
    if not relayer:
        return False, "not_found"
    if (await user.relayers.filter(id=relayer.id).exists()):
        return False, "exists"

    await user.relayers.add(relayer)
    return True, str(relayer.id)


async def remove_relayer(owner_id: int, relayer_identifier: str):
    user = await get_user(owner_id)
    relayer = await get_user(relayer_identifier)
    if not relayer:
        return False, "not_found"
    await user.relayers.remove(relayer)
    return True, str(relayer.id)
