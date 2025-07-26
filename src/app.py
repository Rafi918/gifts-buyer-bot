from pyrogram import Client, filters
from pyrogram.types import PreCheckoutQuery
from config import config
from state import user_state, user_data
from keyboards.reply import get_main_menu

from handlers.main_menu import handle_start
from handlers.charge_stars import handle_charge_stars
from handlers.refund_stars import handle_refund_stars
from handlers.orders import handle_orders
from handlers.send_gift import handle_send_gift

app = Client("star_bot", api_id=config.API_ID,
             api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

STATE_HANDLERS = {
    "awaiting_star_amount": handle_charge_stars,
    "confirming_star_charge": handle_charge_stars,
    "awaiting_refund_id": handle_refund_stars,
    "adding_order": handle_orders,
    "confirming_order": handle_orders,
    "removing_order": handle_orders,
    "awaiting_gift_id": handle_send_gift,
}

BUTTON_HANDLERS = {
    "Charge Stars": handle_charge_stars,
    "Refund Stars": handle_refund_stars,
    "Orders": handle_orders,
    "Add Order": handle_orders,
    "Remove Order": handle_orders,
    "Send Gift": handle_send_gift,
}


def init_handlers(app: Client):
    """Register all Pyrogram handlers."""

    @app.on_pre_checkout_query()
    async def precheckout_callback(client, query: PreCheckoutQuery):
        if query.invoice_payload == "star_charge":
            await query.answer(ok=True)
        else:
            await query.answer(ok=False, error_message="Something went wrong.")

    @app.on_message(filters.command("start"))
    async def start_handler(client, message):
        user_state[message.from_user.id] = None
        await handle_start(client, message)

    @app.on_message(filters.text)
    async def main_handler(client, message):
        user_id = message.from_user.id
        text = message.text.strip()
        state = user_state.get(user_id)

        if text == "Return":
            user_state[user_id] = None
            await message.reply("🔙 Back to main menu.", reply_markup=get_main_menu())
            return

        if text in BUTTON_HANDLERS:
            handler = BUTTON_HANDLERS[text]
            user_state[user_id] = await handler(client, message, state, user_data)
            return

        if state in STATE_HANDLERS:
            handler = STATE_HANDLERS[state]
            user_state[user_id] = await handler(client, message, state, user_data)
            return

        await message.reply("I didn’t understand that. Please use the menu.", reply_markup=get_main_menu())
