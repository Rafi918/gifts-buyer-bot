from pyrogram import Client, filters
from pyrogram.types import Message, PreCheckoutQuery
from config import config
from state import user_state, user_data
from keyboards.reply import get_main_menu
from database.users_crud import get_user_data, add_user
from database.transaction_crud import add_transaction
from handlers.main_menu import handle_start
from routing import BUTTON_HANDLERS, STATE_HANDLERS
from constants.button_action import ButtonAction

from pyrogram.types import CallbackQuery
from handlers.manage_users import update_users_list_page


app = Client("star_bot", api_id=config.API_ID,
             api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)


def init_handlers(app: Client):

    @app.on_pre_checkout_query()
    async def precheckout_callback(client, query: PreCheckoutQuery):
        if query.invoice_payload == "star_charge":
            if (query.currency != "XTR"):
                await query.answer(ok=False, error_message="Invalid currency. Please use XTR.")
                return

            result = await query.answer(ok=True)
        else:
            await query.answer(ok=False, error_message="Something went wrong.")

    @app.on_message(filters.successful_payment)
    async def successful_payment_handler(client: Client, message: Message):
        await add_transaction(message.from_user.id, message.successful_payment.total_amount,
                              message.successful_payment.telegram_payment_charge_id)

    @app.on_message(filters.command("start"))
    async def start_handler(client, message):
        user_id = message.from_user.id
        user_state[user_id] = None
        user_data[user_id] = {}
        user = await get_user_data(user_id)
        role = "receiver"
        if user:
            role = user.role
        if not user and str(user_id) == str(config.ADMIN_ID):
            await add_user(
                user_id=user_id,
                name=message.from_user.first_name or "none",
                username=message.from_user.username or "none",
                role="admin"
            )
            role = "admin"

        await handle_start(client, message, role)

    @app.on_callback_query()
    async def callback_handler(client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id

        user = await get_user_data(user_id)
        if not user and user.role != "admin":
            return
        data = callback_query.data

        await callback_query.answer()

        if data.startswith("next_"):
            page = int(data.split("_")[1]) + 1
            await update_users_list_page(client, callback_query.message, page)

        elif data.startswith("prev_"):
            page = int(data.split("_")[1]) - 1
            await update_users_list_page(client, callback_query.message, page)
        else:
            await callback_query.answer("Unknown action.", show_alert=True)

    @app.on_message(filters.text)
    async def main_handler(client, message):
        user_id = message.from_user.id
        user = await get_user_data(user_id)

        role = "receiver"
        if user:
            role = user.role

        text = message.text.strip()
        state = user_state.get(user_id)

        if (role == "receiver"):
            return

        try:
            action = ButtonAction(text)
            if action == ButtonAction.RETURN:
                user_state[user_id] = None
                await message.reply("🔙 Back to main menu.", reply_markup=get_main_menu(role))
                return

            handler = BUTTON_HANDLERS[action]
            user_state[user_id] = await handler(client, message, state, user_data, role)
            return
        except ValueError:
            pass

        if state in STATE_HANDLERS:
            handler = STATE_HANDLERS[state]
            user_state[user_id] = await handler(client, message, state, user_data, role)
            return

        await message.reply("I didn’t understand that. Please use the menu.", reply_markup=get_main_menu(role))
