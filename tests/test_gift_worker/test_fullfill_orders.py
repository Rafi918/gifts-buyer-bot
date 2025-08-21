# tests/test_fulfill_orders_fallback_userbot.py
import os
import sys
import types
import pytest
from unittest.mock import AsyncMock, MagicMock
pytestmark = pytest.mark.asyncio


class DummySession:
    async def __aenter__(self): return self
    async def __aexit__(self, exc_type, exc, tb): return False


async def test_fulfill_orders_fallbacks_to_userbot_on_bot_error(monkeypatch):
    sys.path.append(os.path.abspath("src"))
    import worker.gift_worker as gw

    # Order needs 1 gift and has enough stars/ranges
    order = types.SimpleNamespace(
        id=1, receiver_id=123,
        user=types.SimpleNamespace(id=7, stars=100),
        count=1, completed_count=0,
        min_stars=0, max_stars=1000, min_supply=0, max_supply=1000,
    )

    # One valid gift
    gifts = [{
        "id": 99, "price": 50, "is_limited": True,
        "available_amount": 5, "total_amount": 20,
    }]

    # Avoid real HTTP
    monkeypatch.setattr(gw.aiohttp, "ClientSession", lambda: DummySession())

    # Data sources
    monkeypatch.setattr(gw, "get_all_orders", AsyncMock(return_value=[order]))
    monkeypatch.setattr(gw, "fetch_gifts", AsyncMock(return_value=gifts))

    # Buyers: bot fails → should trigger userbot fallback
    buy_bot = AsyncMock(side_effect=RuntimeError("bot send failed"))
    buy_user = AsyncMock()
    monkeypatch.setattr(gw, "buy_gift_bot", buy_bot)
    monkeypatch.setattr(gw, "buy_gift_userbot", buy_user)

    # Quiet logs
    monkeypatch.setattr(gw, "worker_logger", MagicMock())

    # Act
    await gw.fulfill_orders(user_bot_id=7)

    # Assert: bot tried once, then userbot tried once
    buy_bot.assert_awaited_once()
    buy_user.assert_awaited_once()


async def test_fulfill_orders_no_fallback_if_different_user(monkeypatch):
    sys.path.append(os.path.abspath("src"))
    import worker.gift_worker as gw

    order = types.SimpleNamespace(
        id=1, receiver_id=123,
        user=types.SimpleNamespace(id=7, stars=100),
        count=1, completed_count=0,
        min_stars=0, max_stars=1000, min_supply=0, max_supply=1000,
    )

    gifts = [{
        "id": 99, "price": 50, "is_limited": True,
        "available_amount": 5, "total_amount": 20,
    }]

    monkeypatch.setattr(gw.aiohttp, "ClientSession", lambda: DummySession())
    monkeypatch.setattr(gw, "get_all_orders", AsyncMock(return_value=[order]))
    monkeypatch.setattr(gw, "fetch_gifts", AsyncMock(return_value=gifts))

    buy_bot = AsyncMock(side_effect=RuntimeError("bot send failed"))
    buy_user = AsyncMock()
    monkeypatch.setattr(gw, "buy_gift_bot", buy_bot)
    monkeypatch.setattr(gw, "buy_gift_userbot", buy_user)
    monkeypatch.setattr(gw, "worker_logger", MagicMock())

    # Act
    await gw.fulfill_orders(user_bot_id=80)  # falsy!

    # Assert: bot tried, but no userbot attempt without id
    buy_bot.assert_awaited_once()
    buy_user.assert_not_awaited()



async def test_fulfill_orders_no_fallback_if_no_userbot_id(monkeypatch):
    sys.path.append(os.path.abspath("src"))
    import worker.gift_worker as gw

    order = types.SimpleNamespace(
        id=1, receiver_id=123,
        user=types.SimpleNamespace(id=7, stars=100),
        count=1, completed_count=0,
        min_stars=0, max_stars=1000, min_supply=0, max_supply=1000,
    )

    gifts = [{
        "id": 99, "price": 50, "is_limited": True,
        "available_amount": 5, "total_amount": 20,
    }]

    monkeypatch.setattr(gw.aiohttp, "ClientSession", lambda: DummySession())
    monkeypatch.setattr(gw, "get_all_orders", AsyncMock(return_value=[order]))
    monkeypatch.setattr(gw, "fetch_gifts", AsyncMock(return_value=gifts))

    buy_bot = AsyncMock(side_effect=RuntimeError("bot send failed"))
    buy_user = AsyncMock()
    monkeypatch.setattr(gw, "buy_gift_bot", buy_bot)
    monkeypatch.setattr(gw, "buy_gift_userbot", buy_user)
    monkeypatch.setattr(gw, "worker_logger", MagicMock())

    # Act
    await gw.fulfill_orders(user_bot_id=None)  # falsy!

    # Assert: bot tried, but no userbot attempt without id
    buy_bot.assert_awaited_once()
    buy_user.assert_not_awaited()


async def test_fulfill_orders_multiple_orders(monkeypatch):
    sys.path.append(os.path.abspath("src"))
    import worker.gift_worker as gw

    # --- Arrange ---
    order1 = types.SimpleNamespace(
        id=1, receiver_id=111,
        user=types.SimpleNamespace(id=7, stars=10_000),
        count=5, completed_count=0,
        min_stars=0, max_stars=20_000,
        min_supply=0, max_supply=50_000,
    )
    order2 = types.SimpleNamespace(
        id=2, receiver_id=222,
        user=types.SimpleNamespace(id=8, stars=2_000_000),
        count=100, completed_count=0,
        min_stars=0, max_stars=5_000_000,
        min_supply=0, max_supply=50_000,
    )

    gift1 = {"id": 10, "price": 10_000, "is_limited": True,
             "available_amount": 1000, "total_amount": 1000}
    gift2 = {"id": 20, "price": 300, "is_limited": True,
             "available_amount": 20_000, "total_amount": 20_000}

    # Avoid real HTTP
    monkeypatch.setattr(gw.aiohttp, "ClientSession", lambda: DummySession())
    monkeypatch.setattr(gw, "get_all_orders", AsyncMock(
        return_value=[order1, order2]))
    monkeypatch.setattr(gw, "fetch_gifts", AsyncMock(
        return_value=[gift1, gift2]))

    # Buyers
    buy_bot = AsyncMock()
    monkeypatch.setattr(gw, "buy_gift_bot", buy_bot)
    monkeypatch.setattr(gw, "buy_gift_userbot", AsyncMock())

    # Quiet logs
    monkeypatch.setattr(gw, "worker_logger", MagicMock())

    # --- Act ---
    await gw.fulfill_orders(user_bot_id=999)

    # --- Assert ---
    # order1 needed 5 * 2 gifts → 10 calls
    # order2 needed 100 * 2 gifts → 200 calls
    assert buy_bot.await_count == 210

    # Optionally check the call args for both orders
    order1_calls = [c for c in buy_bot.await_args_list if c.args[1].id == 1]
    order2_calls = [c for c in buy_bot.await_args_list if c.args[1].id == 2]

    assert len(order1_calls) == 10
    assert len(order2_calls) == 200
