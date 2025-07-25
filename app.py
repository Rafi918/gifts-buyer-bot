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

app = Client("star_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)


def init_handlers(app):
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

        if text == "Charge Stars" or state in ["awaiting_star_amount", "confirming_star_charge"]:
            user_state[user_id] = await handle_charge_stars(client, message, state, user_data)

        elif text == "Refund Stars" or state == "awaiting_refund_id":
            user_state[user_id] = await handle_refund_stars(client, message, state)

        elif text in ["Orders", "Add Order", "Remove Order"] or state in ["adding_order", "confirming_order", "removing_order"]:
            user_state[user_id] = await handle_orders(client, message, state, user_data)

        elif text == "Send Gift" or state == "awaiting_gift_id":
            user_state[user_id] = await handle_send_gift(client, message, state)
