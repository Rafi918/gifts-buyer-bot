from database.crud import add_order, get_orders, remove_order
from constants.texts import TEXTS
from keyboards.reply import (
    get_orders_menu,
    get_order_remove_keyboard,
    get_confirmation_menu,
    get_return_menu,
    get_main_menu
)


async def handle_orders(client, message, state, user_data):
    user_id = message.from_user.id
    text = message.text.strip()

    # 🔄 Step 1: Adding order (user inputs order details)
    if state == "adding_order":
        parts = text.split()
        if len(parts) == 7 and parts[0].lower() == "auto" and all(p.isdigit() for p in parts[1:]):
            _, min_stars, max_stars, min_supply, max_supply, count, receiver_id = parts
            user_data[user_id] = {
                "order": (int(min_stars), int(max_stars), int(min_supply), int(max_supply), int(count), int(receiver_id))
            }
            await message.reply(TEXTS["add_order_confirm"].format(min_stars, max_stars, min_supply, max_supply, count, receiver_id), reply_markup=get_confirmation_menu())
            return "confirming_order"
        else:
            await message.reply(TEXTS["invalid_format"], reply_markup=get_return_menu())
            return "adding_order"

    # 🔄 Step 2: Confirming order (user confirms "Yes" or "No")
    if state == "confirming_order":
        if text == "Yes":
            await add_order(user_id, *user_data[user_id]["order"])
            await message.reply("✅ Order added.", reply_markup=get_main_menu())
            return None
        if text == "No":
            await message.reply("❌ Order cancelled. Enter a new order:", reply_markup=get_return_menu())
            return "adding_order"
        else:
            await message.reply("Please confirm with 'Yes' or 'No'.", reply_markup=get_confirmation_menu())
            return "confirming_order"

    # 🔄 Step 3: Removing an order
    if state == "removing_order" and text.isdigit():
        orders = await get_orders(user_id)
        index = int(text) - 1
        if 0 <= index < len(orders):
            await remove_order(user_id, orders[index].id)
            await message.reply("✅ Order removed.", reply_markup=get_main_menu())
        else:
            await message.reply("❌ Invalid order number.", reply_markup=get_main_menu())
        return None

    # ➕ User clicked "Add Order"
    if text == "Add Order":
        await message.reply(
            TEXTS["add_order_format"],
            reply_markup=get_return_menu()
        )
        return "adding_order"

    # 🗑️ User clicked "Remove Order"
    if text == "Remove Order":
        orders = await get_orders(user_id)
        if not orders:
            await message.reply(TEXTS["orders_empty"], reply_markup=get_orders_menu())
            return None
        order_list = "\n".join(
            [f"{i+1}. {str(o)}" for i, o in enumerate(orders)]
        )
        await message.reply(
            f"📦 Your current orders:\n{order_list}\n\n🗑️ Send the number of the order you want to remove:",
            reply_markup=get_return_menu()
        )
        return "removing_order"

    # 📋 User clicked "Orders"
    if text == "Orders" or state is None:
        orders = await get_orders(user_id)
        if not orders:
            await message.reply(TEXTS["orders_empty"], reply_markup=get_orders_menu())
        else:
            order_list = "\n".join(
                [f"{i+1}. {str(o)}" for i, o in enumerate(orders)]
            )
            await message.reply(TEXTS["orders_list"].format(order_list), reply_markup=get_orders_menu())
        return "orders_menu"

    return state
