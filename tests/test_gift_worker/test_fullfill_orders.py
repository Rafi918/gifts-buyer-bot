# tests/test_gift_worker/test_fulfill_orders.py
import os
import sys
import types
import pytest
from unittest.mock import AsyncMock, MagicMock

pytestmark = pytest.mark.asyncio


class DummySession:
    async def __aenter__(self): return self
    async def __aexit__(self, exc_type, exc, tb): return False


def make_order(order_id, user_id, stars, count, completed=0,
               min_stars=0, max_stars=10**9,
               min_supply=0, max_supply=10**9, receiver_id=None):
    """Helper to build fake Order with nested fake User"""
    return types.SimpleNamespace(
        id=order_id,
        receiver_id=receiver_id or order_id * 100,
        user=types.SimpleNamespace(id=user_id, stars=stars),
        count=count,
        completed_count=completed,
        min_stars=min_stars,
        max_stars=max_stars,
        min_supply=min_supply,
        max_supply=max_supply,
    )


async def test_fulfill_orders_no_valid_gifts(monkeypatch):
    sys.path.append(os.path.abspath("src"))
    import worker.gift_worker as gw

    order = make_order(order_id=1, user_id=7, stars=100, count=1)
    gifts = [{"id": 1, "price": 50, "is_limited": False,
              "available_amount": 0, "total_amount": 0}]

    monkeypatch.setattr(gw, "notify_users", AsyncMock())
    monkeypatch.setattr(gw.aiohttp, "ClientSession", lambda: DummySession())
    monkeypatch.setattr(gw, "get_all_orders", AsyncMock(return_value=[order]))
    monkeypatch.setattr(gw, "fetch_gifts", AsyncMock(return_value=gifts))
    buy_bot = AsyncMock()
    monkeypatch.setattr(gw, "try_buying_gift", buy_bot)
    monkeypatch.setattr(gw, "worker_logger", MagicMock())

    await gw.fulfill_orders(user_bot_id=7)

    buy_bot.assert_not_awaited()
    gw.notify_users.assert_not_awaited()


async def test_fulfill_orders_skips_completed_orders(monkeypatch):
    sys.path.append(os.path.abspath("src"))
    import worker.gift_worker as gw

    order = make_order(order_id=1, user_id=7, stars=100, count=5, completed=5)
    gifts = [{"id": 1, "price": 50, "is_limited": True,
              "available_amount": 10, "total_amount": 10}]

    monkeypatch.setattr(gw, "notify_users", AsyncMock())
    monkeypatch.setattr(gw.aiohttp, "ClientSession", lambda: DummySession())
    monkeypatch.setattr(gw, "get_all_orders", AsyncMock(return_value=[order]))
    monkeypatch.setattr(gw, "fetch_gifts", AsyncMock(return_value=gifts))
    buy_bot = AsyncMock()
    monkeypatch.setattr(gw, "try_buying_gift", buy_bot)
    monkeypatch.setattr(gw, "worker_logger", MagicMock())

    await gw.fulfill_orders(user_bot_id=7)

    buy_bot.assert_not_awaited()


async def test_fulfill_orders_skips_when_price_out_of_range(monkeypatch):
    sys.path.append(os.path.abspath("src"))
    import worker.gift_worker as gw

    order = make_order(order_id=1, user_id=7, stars=100,
                       count=1, min_stars=200, max_stars=300)
    gifts = [{"id": 2, "price": 50, "is_limited": True,
              "available_amount": 5, "total_amount": 10}]

    monkeypatch.setattr(gw, "notify_users", AsyncMock())
    monkeypatch.setattr(gw.aiohttp, "ClientSession", lambda: DummySession())
    monkeypatch.setattr(gw, "get_all_orders", AsyncMock(return_value=[order]))
    monkeypatch.setattr(gw, "fetch_gifts", AsyncMock(return_value=gifts))
    buy_bot = AsyncMock()
    monkeypatch.setattr(gw, "try_buying_gift", buy_bot)
    monkeypatch.setattr(gw, "worker_logger", MagicMock())

    await gw.fulfill_orders(user_bot_id=7)

    buy_bot.assert_not_awaited()


async def test_fulfill_orders_skips_when_supply_out_of_range(monkeypatch):
    sys.path.append(os.path.abspath("src"))
    import worker.gift_worker as gw

    order = make_order(order_id=1, user_id=7, stars=100,
                       count=1, min_supply=200, max_supply=300)
    gifts = [{"id": 3, "price": 50, "is_limited": True,
              "available_amount": 5, "total_amount": 10}]

    monkeypatch.setattr(gw, "notify_users", AsyncMock())
    monkeypatch.setattr(gw.aiohttp, "ClientSession", lambda: DummySession())
    monkeypatch.setattr(gw, "get_all_orders", AsyncMock(return_value=[order]))
    monkeypatch.setattr(gw, "fetch_gifts", AsyncMock(return_value=gifts))
    buy_bot = AsyncMock()
    monkeypatch.setattr(gw, "try_buying_gift", buy_bot)
    monkeypatch.setattr(gw, "worker_logger", MagicMock())

    await gw.fulfill_orders(user_bot_id=7)

    buy_bot.assert_not_awaited()


async def test_fulfill_orders_multiple_orders(monkeypatch):
    sys.path.append(os.path.abspath("src"))
    import worker.gift_worker as gw

    order1 = make_order(order_id=1, user_id=7, stars=10_000,
                        count=5, min_stars=0, max_stars=20_000,
                        min_supply=0, max_supply=50_000)
    order2 = make_order(order_id=2, user_id=8, stars=2_000_000,
                        count=100, min_stars=0, max_stars=5_000_000,
                        min_supply=0, max_supply=50_000)

    gift1 = {"id": 10, "price": 10_000, "is_limited": True,
             "available_amount": 1000, "total_amount": 1000}
    gift2 = {"id": 20, "price": 300, "is_limited": True,
             "available_amount": 20_000, "total_amount": 20_000}

    monkeypatch.setattr(gw, "notify_users", AsyncMock())
    monkeypatch.setattr(gw.aiohttp, "ClientSession", lambda: DummySession())
    monkeypatch.setattr(gw, "get_all_orders", AsyncMock(
        return_value=[order1, order2]))
    monkeypatch.setattr(gw, "fetch_gifts", AsyncMock(
        return_value=[gift1, gift2]))

    buy_bot = AsyncMock()
    monkeypatch.setattr(gw, "try_buying_gift", buy_bot)
    monkeypatch.setattr(gw, "worker_logger", MagicMock())

    await gw.fulfill_orders(user_bot_id=999)

    assert buy_bot.await_count == 210

    # Unpack args more clearly
    order_calls = [c.args[3] for c in buy_bot.await_args_list]
    order1_calls = [o for o in order_calls if o.id == 1]
    order2_calls = [o for o in order_calls if o.id == 2]

    assert len(order1_calls) == 10
    assert len(order2_calls) == 200


async def test_fulfill_orders_multiple_orders_v2(monkeypatch):
    sys.path.append(os.path.abspath("src"))
    import worker.gift_worker as gw

    order1 = make_order(order_id=1, user_id=7, stars=10_000,
                        count=5, min_stars=0, max_stars=20_000,
                        min_supply=0, max_supply=5_000)
    order2 = make_order(order_id=2, user_id=8, stars=2_000_000,
                        count=100, min_stars=0, max_stars=5_000_000,
                        min_supply=0, max_supply=50_000)

    gift1 = {"id": 10, "price": 10_000, "is_limited": True,
             "available_amount": 1000, "total_amount": 1000}
    gift2 = {"id": 20, "price": 300, "is_limited": True,
             "available_amount": 20_000, "total_amount": 20_000}

    monkeypatch.setattr(gw, "notify_users", AsyncMock())
    monkeypatch.setattr(gw.aiohttp, "ClientSession", lambda: DummySession())
    monkeypatch.setattr(gw, "get_all_orders", AsyncMock(
        return_value=[order1, order2]))
    monkeypatch.setattr(gw, "fetch_gifts", AsyncMock(
        return_value=[gift1, gift2]))

    buy_bot = AsyncMock()
    monkeypatch.setattr(gw, "try_buying_gift", buy_bot)
    monkeypatch.setattr(gw, "worker_logger", MagicMock())

    await gw.fulfill_orders(user_bot_id=999)

    assert buy_bot.await_count == 205

    # Unpack args more clearly
    order_calls = [c.args[3] for c in buy_bot.await_args_list]
    order1_calls = [o for o in order_calls if o.id == 1]
    order2_calls = [o for o in order_calls if o.id == 2]

    assert len(order1_calls) == 5
    assert len(order2_calls) == 200
