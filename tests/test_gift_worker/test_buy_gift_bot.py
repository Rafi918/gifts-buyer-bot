import types
import pytest
from unittest.mock import AsyncMock

pytestmark = pytest.mark.asyncio


async def test_buy_gift_bot_does_nothing_when_not_enough_stars(monkeypatch):
    # Import your worker module so we can patch things where they're used
    import sys
    import os
    sys.path.append(os.path.abspath("src"))

    import worker.gift_worker as gw
    from worker.errors import InsufficientStarsError

    # Patch side-effect functions with async mocks
    monkeypatch.setattr(gw.app, "send_gift", AsyncMock())
    monkeypatch.setattr(gw, "deduct_user_stars", AsyncMock())
    monkeypatch.setattr(gw, "increment_completed_count", AsyncMock())
    monkeypatch.setattr(gw, "get_user_data", AsyncMock())

    # Gift costs more than the user has → should be a no-op
    gift = {"id": 1, "price": 200}
    order = types.SimpleNamespace(
        id=123,
        receiver_id=555,
        user=types.SimpleNamespace(id=42, stars=100),
    )

    with pytest.raises(InsufficientStarsError):
        await gw.buy_gift_bot(gift, order)

    # Assert NOTHING was called
    gw.app.send_gift.assert_not_awaited()
    gw.deduct_user_stars.assert_not_awaited()
    gw.increment_completed_count.assert_not_awaited()
    gw.get_user_data.assert_not_awaited()


async def test_buy_gift_bot_happy_path(monkeypatch):
    # Make src importable
    import sys
    import os
    sys.path.append(os.path.abspath("src"))

    import worker.gift_worker as gw

    # Arrange: user has enough stars
    gift = {"id": 7, "price": 50}
    order = types.SimpleNamespace(
        id=123,
        receiver_id=555,
        user=types.SimpleNamespace(id=42, stars=100),
    )

    # Mocks
    send_gift_mock = AsyncMock(name="send_gift")
    deduct_mock = AsyncMock(name="deduct_user_stars", return_value=True)
    increment_mock = AsyncMock(
        name="increment_completed_count", return_value=order)
    get_user_mock = AsyncMock(name="get_user_data", return_value=order.user)

    # Patch where used
    monkeypatch.setattr(gw.app, "send_gift", send_gift_mock)
    monkeypatch.setattr(gw, "deduct_user_stars", deduct_mock)
    monkeypatch.setattr(gw, "increment_completed_count", increment_mock)
    monkeypatch.setattr(gw, "get_user_data", get_user_mock)

    # Act
    await gw.buy_gift_bot(gift, order)

    # Assert: correct side effects happened exactly once
    send_gift_mock.assert_awaited_once_with(chat_id=555, gift_id=7)
    deduct_mock.assert_awaited_once_with(42, 50)
    increment_mock.assert_awaited_once_with(123)
    get_user_mock.assert_awaited_once_with(42)
