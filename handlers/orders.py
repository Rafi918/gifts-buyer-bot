import json
import os
from keyboards.reply import (
    get_orders_menu,
    get_order_remove_keyboard,
    get_confirmation_menu,
    get_return_menu,
    get_main_menu
)
from constants.texts import TEXTS

ORDERS_FILE = "data/orders.json"

# ✅ Load orders from file


def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return {}
    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# ✅ Save orders to file


def save_orders(data):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


orders_store = load_orders()


async def handle_orders(client, message, state, user_data):
    user_id = str(message.from_user.id)  # Store user_id as str for JSON
    text = message.text.strip()

    if state == "adding_order":
        parts = text.split()
        if len(parts) == 6 and parts[0].lower() == "auto" and all(p.isdigit() for p in parts[1:5]):
            user_data[user_id] = {"new_order": text}
            await message.reply(TEXTS["add_order_confirm"].format(text), reply_markup=get_confirmation_menu())
            return "confirming_order"
        else:
            await message.reply(TEXTS["invalid_format"])
            return "adding_order"

    elif state == "confirming_order":
        if text == "Yes":
            order = user_data[user_id]["new_order"]
            orders_store.setdefault(user_id, []).append(order)
            save_orders(orders_store)
            await message.reply("✅ Order added.", reply_markup=get_main_menu())
            return None
        elif text == "No":
            await message.reply("❌ Order cancelled. Enter a new order:", reply_markup=get_return_menu())
            return "adding_order"
        else:
            await message.reply("Please confirm with 'Yes' or 'No'.", reply_markup=get_confirmation_menu())
            return "confirming_order"

    elif state == "removing_order" and text.isdigit():
        index = int(text) - 1
        if 0 <= index < len(orders_store.get(user_id, [])):
            removed = orders_store[user_id].pop(index)
            save_orders(orders_store)
            await message.reply(f"✅ Removed order: {removed}", reply_markup=get_main_menu())
        else:
            await message.reply("❌ Invalid order number.", reply_markup=get_main_menu())
        return None

    elif text == "Add Order":
        await message.reply(TEXTS["add_order_format"], reply_markup=get_return_menu())
        return "adding_order"

    elif text == "Remove Order":
        user_orders = orders_store.get(user_id, [])
        if not user_orders:
            await message.reply(TEXTS["orders_empty"], reply_markup=get_orders_menu())
            return None
        await message.reply("Select the number of the order to remove:", reply_markup=get_order_remove_keyboard(len(user_orders)))
        return "removing_order"

    elif text == "Orders" or state is None:
        user_orders = orders_store.get(user_id, [])
        if not user_orders:
            await message.reply(TEXTS["orders_empty"], reply_markup=get_orders_menu())
        else:
            order_list = "\n".join(
                [f"{i+1}. {o}" for i, o in enumerate(user_orders)])
            await message.reply(TEXTS["orders_list"].format(order_list), reply_markup=get_orders_menu())
        return None

    return state
