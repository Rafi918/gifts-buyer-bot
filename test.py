from pyrogram import Client, filters
from pyrogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Message
)

API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
BOT_TOKEN = "7985667788:AAHXiBeom0QVxjd2C9Wb3zffnZRzBoQ4pbg"

app = Client("star_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# In-memory storage
user_state = {}
user_data = {}
orders = {}

# Keyboards
main_menu = ReplyKeyboardMarkup(
    [["Charge Stars", "Refund Stars"], ["Orders"]],
    resize_keyboard=True
)

back_button = ReplyKeyboardMarkup([["Return"]], resize_keyboard=True)


def get_orders_keyboard(user_id):
    user_orders = orders.get(user_id, [])
    keyboard = [[str(i+1)] for i in range(len(user_orders))]
    keyboard.append(["Return"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


@app.on_message(filters.command("start"))
async def start(client, message: Message):
    user_state[message.from_user.id] = None
    await message.reply("Welcome! Choose an option:", reply_markup=main_menu)


@app.on_message(filters.text)
async def handle_text(client, message: Message):
    user_id = message.from_user.id
    text = message.text

    state = user_state.get(user_id)

    if text == "Return":
        user_state[user_id] = None
        await message.reply("Back to main menu.", reply_markup=main_menu)

    elif text == "Charge Stars":
        user_state[user_id] = "awaiting_star_amount"
        await message.reply("Enter the number of stars you want to charge:", reply_markup=back_button)

    elif state == "awaiting_star_amount":
        if not text.isdigit():
            await message.reply("Please enter a valid number.")
            return
        user_data[user_id] = {"charge_stars": int(text)}
        user_state[user_id] = "confirming_star_charge"
        await message.reply(f"Do you want to charge {text} stars?",
                            reply_markup=ReplyKeyboardMarkup([["Yes", "No"], ["Return"]], resize_keyboard=True))

    elif state == "confirming_star_charge":
        if text == "Yes":
            stars = user_data[user_id]["charge_stars"]
            await message.reply(f"{stars} stars have been charged.", reply_markup=main_menu)
            user_state[user_id] = None
        elif text == "No":
            await message.reply("Operation cancelled.", reply_markup=main_menu)
            user_state[user_id] = None

    elif text == "Refund Stars":
        user_state[user_id] = "awaiting_refund_tx"
        await message.reply("Please send the transaction ID to refund:", reply_markup=back_button)

    elif state == "awaiting_refund_tx":
        tx_id = text
        await message.reply(f"Refund processed for transaction: {tx_id}", reply_markup=main_menu)
        user_state[user_id] = None

    elif text == "Orders":
        user_orders = orders.get(user_id, [])
        if not user_orders:
            await message.reply("You have no orders.",
                                reply_markup=ReplyKeyboardMarkup([["Add Order", "Return"]], resize_keyboard=True))
        else:
            order_texts = [f"{i+1}. {o}" for i, o in enumerate(user_orders)]
            await message.reply("Your orders:\n" + "\n".join(order_texts),
                                reply_markup=ReplyKeyboardMarkup([["Add Order", "Remove Order"], ["Return"]], resize_keyboard=True))

    elif text == "Add Order":
        user_state[user_id] = "awaiting_order_input"
        await message.reply("Enter order in format:\nauto min max supply count receiver", reply_markup=back_button)

    elif state == "awaiting_order_input":
        parts = text.strip().split()
        if len(parts) != 6 or parts[0].lower() != "auto":
            await message.reply("Invalid format. Try again.\nFormat: auto min max supply count receiver")
            return
        user_data[user_id] = {"order": text}
        user_state[user_id] = "confirming_add_order"
        await message.reply(f"So you want to add this order?\n{text}",
                            reply_markup=ReplyKeyboardMarkup([["Yes", "No"], ["Return"]], resize_keyboard=True))

    elif state == "confirming_add_order":
        if text == "Yes":
            order = user_data[user_id]["order"]
            orders.setdefault(user_id, []).append(order)
            await message.reply("Order added.", reply_markup=main_menu)
            user_state[user_id] = None
        elif text == "No":
            user_state[user_id] = "awaiting_order_input"
            await message.reply("Re-enter the order:", reply_markup=back_button)

    elif text == "Remove Order":
        user_orders = orders.get(user_id, [])
        if not user_orders:
            await message.reply("You have no orders to remove.", reply_markup=main_menu)
            return
        user_state[user_id] = "awaiting_remove_index"
        await message.reply("Select the order number to remove:", reply_markup=get_orders_keyboard(user_id))

    elif state == "awaiting_remove_index":
        if text.isdigit():
            idx = int(text) - 1
            if 0 <= idx < len(orders.get(user_id, [])):
                removed = orders[user_id].pop(idx)
                await message.reply(f"Removed order: {removed}", reply_markup=main_menu)
                user_state[user_id] = None
            else:
                await message.reply("Invalid order number.")
        else:
            await message.reply("Please send a number corresponding to the order.")


app.run()
