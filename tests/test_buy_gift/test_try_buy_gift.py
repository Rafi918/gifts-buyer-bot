# tests/test_try_buy_gift.py
import os
import sys
import types
import pytest
from unittest.mock import AsyncMock, MagicMock

pytestmark = pytest.mark.asyncio


@pytest.fixture(autouse=True)
def add_src_path():
    sys.path.append(os.path.abspath("src"))


async def test_try_buying_gift_bot_success(monkeypatch):
    import helpers.buy_gift as gw

    gift = {"id": 1, "price": 10}
    order = types.SimpleNamespace(
        id=100,
        receiver_id=555,
        user=types.SimpleNamespace(id=42, stars=50),
    )

    updated_order = types.SimpleNamespace(id=100, user=order.user)

    buy_bot = AsyncMock(return_value=updated_order)
    buy_user = AsyncMock()
    monkeypatch.setattr(gw, "buy_gift_bot", buy_bot)
    monkeypatch.setattr(gw, "buy_gift_userbot", buy_user)

    result = await gw.try_buying_gift("app", "userbot", gift, order, user_bot_id=42)

    assert result is updated_order
    buy_bot.assert_awaited_once_with("app", gift, order)
    buy_user.assert_not_awaited()


async def test_try_buying_gift_bot_fails_fallback_userbot(monkeypatch):
    import helpers.buy_gift as gw

    gift = {"id": 2, "price": 20}
    order = types.SimpleNamespace(
        id=200,
        receiver_id=666,
        user=types.SimpleNamespace(id=77, stars=5),
    )

    buy_bot = AsyncMock(side_effect=RuntimeError("bot error"))
    updated_order = types.SimpleNamespace(id=200, user=order.user)
    buy_user = AsyncMock(return_value=updated_order)

    monkeypatch.setattr(gw, "buy_gift_bot", buy_bot)
    monkeypatch.setattr(gw, "buy_gift_userbot", buy_user)
    monkeypatch.setattr(gw, "worker_logger", MagicMock())

    result = await gw.try_buying_gift("app", "userbot", gift, order, user_bot_id=77)

    assert result is updated_order
    buy_bot.assert_awaited_once()
    buy_user.assert_awaited_once_with("userbot", gift, order)


async def test_try_buying_gift_bot_fails_no_fallback_different_user(monkeypatch):
    import helpers.buy_gift as gw

    gift = {"id": 3, "price": 15}
    order = types.SimpleNamespace(
        id=300,
        receiver_id=777,
        user=types.SimpleNamespace(id=10, stars=5),
    )

    buy_bot = AsyncMock(side_effect=RuntimeError("bot error"))
    buy_user = AsyncMock()

    monkeypatch.setattr(gw, "buy_gift_bot", buy_bot)
    monkeypatch.setattr(gw, "buy_gift_userbot", buy_user)
    monkeypatch.setattr(gw, "worker_logger", MagicMock())

    result = await gw.try_buying_gift("app", "userbot", gift, order, user_bot_id=99)

    assert result is None
    buy_bot.assert_awaited_once()
    buy_user.assert_not_awaited()


async def test_try_buying_gift_bot_fails_no_fallback_none_id(monkeypatch):
    import helpers.buy_gift as gw

    gift = {"id": 4, "price": 25}
    order = types.SimpleNamespace(
        id=400,
        receiver_id=888,
        user=types.SimpleNamespace(id=123, stars=5),
    )

    buy_bot = AsyncMock(side_effect=RuntimeError("bot error"))
    buy_user = AsyncMock()

    monkeypatch.setattr(gw, "buy_gift_bot", buy_bot)
    monkeypatch.setattr(gw, "buy_gift_userbot", buy_user)
    monkeypatch.setattr(gw, "worker_logger", MagicMock())

    result = await gw.try_buying_gift("app", "userbot", gift, order, user_bot_id=None)

    assert result is None
    buy_bot.assert_awaited_once()
    buy_user.assert_not_awaited()


async def test_try_buying_gift_bot_and_userbot_fail(monkeypatch):
    import helpers.buy_gift as gw

    gift = {"id": 5, "price": 30}
    order = types.SimpleNamespace(
        id=500,
        receiver_id=999,
        user=types.SimpleNamespace(id=321, stars=5),
    )

    buy_bot = AsyncMock(side_effect=RuntimeError("bot error"))
    buy_user = AsyncMock(side_effect=RuntimeError("userbot error"))

    monkeypatch.setattr(gw, "buy_gift_bot", buy_bot)
    monkeypatch.setattr(gw, "buy_gift_userbot", buy_user)
    monkeypatch.setattr(gw, "worker_logger", MagicMock())

    result = await gw.try_buying_gift("app", "userbot", gift, order, user_bot_id=321)

    assert result is None
    buy_bot.assert_awaited_once()
    buy_user.assert_awaited_once_with("userbot", gift, order)
