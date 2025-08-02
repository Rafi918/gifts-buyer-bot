from database.orders_crud import add_order, get_orders, remove_order, get_orders_count
from database.users_crud import get_user_data
from constants.texts import TEXTS
from constants.states import States
from constants.button_action import ButtonAction
from keyboards.reply import (
    get_orders_menu,
    get_confirmation_menu,
    get_return_menu,
    get_main_menu
)


async def handle_orders(client, message, state, user_data, role):
    user_id = message.from_user.id
    text = message.text.strip()

    if state == States.ADDING_ORDER:
        parts = text.split()
        if len(parts) == 6 and all(p.isdigit() for p in parts[1:]):
            min_stars, max_stars, min_supply, max_supply, count, receiver_id = parts

            receiver = await get_user_data(receiver_id)

            if not receiver:
                await message.reply(TEXTS["user_not_found"].format(receiver_id), reply_markup=get_return_menu())
                return States.ADDING_ORDER

            user_data[user_id] = {
                "order": (int(min_stars), int(max_stars), int(min_supply), int(max_supply), int(count), int(receiver_id))
            }
            await message.reply(TEXTS["add_order_confirm"].format(min_stars, max_stars, min_supply, max_supply, count, receiver_id), reply_markup=get_confirmation_menu())
            return States.CONFIRMING_ORDER

        await message.reply(TEXTS["invalid_format"], reply_markup=get_return_menu())
        return States.ADDING_ORDER

    if state == States.CONFIRMING_ORDER:
        if text == "Yes":
            await add_order(user_id, *user_data[user_id]["order"])
            await message.reply(TEXTS["order_added"], reply_markup=get_main_menu(role))
            return None
        if text == "No":
            await message.reply(TEXTS["order_cancelled"], reply_markup=get_return_menu())
            return States.ADDING_ORDER
        else:
            await message.reply(TEXTS["order_confirm_prompt"], reply_markup=get_confirmation_menu())
            return States.CONFIRMING_ORDER

    if state == States.REMOVING_ORDER and text.isdigit():
        orders = await get_orders(user_id)
        index = int(text) - 1
        if 0 <= index < len(orders):
            await remove_order(user_id, orders[index].id)
            await message.reply(TEXTS["order_removed"], reply_markup=get_main_menu(role))
        else:
            await message.reply(TEXTS["invalid_order_number"], reply_markup=get_main_menu(role))
        return None

    if text == ButtonAction.ADD_ORDER.value:
        orders_count = await get_orders_count(user_id)
        if (orders_count >= 5):
            await message.reply(TEXTS["max_orders_reached"], reply_markup=get_orders_menu())
            return None
        await message.reply(
            TEXTS["add_order_format"],
            reply_markup=get_return_menu()
        )
        return States.ADDING_ORDER

    if text == ButtonAction.REMOVE_ORDER.value:
        orders = await get_orders(user_id)
        if not orders:
            await message.reply(TEXTS["orders_empty"], reply_markup=get_orders_menu())
            return None
        order_list = "\n".join(
            [f"{i+1}. {str(o)}" for i, o in enumerate(orders)]
        )
        await message.reply(
            TEXTS["remove_order_prompt"].format(order_list),
            reply_markup=get_return_menu()
        )
        return States.REMOVING_ORDER

    if text == ButtonAction.ORDERS.value or state is None:
        orders = await get_orders(user_id)
        if not orders:
            await message.reply(TEXTS["orders_empty"], reply_markup=get_orders_menu())
        else:
            order_list = "\n".join(
                [f"{i+1}. {str(o)}" for i, o in enumerate(orders)]
            )
            await message.reply(TEXTS["orders_list"].format(order_list), reply_markup=get_orders_menu())
        return States.ORDERS_MENU

    return state
