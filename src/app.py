from pyrogram import Client, filters
from pyrogram.types import Message, PreCheckoutQuery
from config import config
from state import user_state, user_data
from keyboards.reply import get_main_menu
from database.users_crud import get_user_data, add_user, update_data
from database.transaction_crud import add_transaction
from database.orders_crud import get_orders
from handlers.main_menu import handle_start
from routing import BUTTON_HANDLERS, STATE_HANDLERS
from constants.button_action import ButtonAction

from pyrogram.types import CallbackQuery
from handlers.manage_users import update_users_list_page
from constants.texts import TEXTS
from constants.roles import Roles

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
        if (message.chat.type != "ChatType.CHANNEL"):
            user = await get_user_data(message.chat.id)
            if (user):
                return await message.reply(TEXTS["channel_already_added"].format(message.chat.id))

            await add_user(
                user_id=message.chat.id,
                name=message.chat.title or "none",
                username=message.chat.username or "none",
                role=Roles.RECEIVER.value
            )
            return await message.reply(TEXTS["adding_channel"].format(message.chat.id))

        user_id = message.from_user.id
        if (user_id not in user_state) or user_id not in user_data:
            user_state[user_id] = None
            user_data[user_id] = {}
        user = await get_user_data(user_id)
        role = Roles.RECEIVER

        if user:
            role = Roles(user.role)
            if (user.name == "Unknown"):
                await update_data(user_id=user_id, name=message.from_user.first_name or "none", username=message.from_user.username or "none")
        if not user and str(user_id) == str(config.ADMIN_ID):
            await add_user(
                user_id=user_id,
                name=message.from_user.first_name or "none",
                username=message.from_user.username or "none",
                role=Roles.Admin.value
            )
            role = Roles.Admin

        await handle_start(client, message, role)

    @app.on_message(filters.command("me"))
    async def profile_handler(client, message):
        user_id = message.from_user.id
        user = await get_user_data(user_id)
        if not user or user.role == Roles.RECEIVER.value:
            await message.reply(TEXTS["profile_user"].format(user_id))
            return
        orders = await get_orders(user_id)

        order_list = "\n".join(
            [f"{i+1}. {str(o)}" for i, o in enumerate(orders)])

        orders_text = TEXTS["orders_list"].format(
            order_list) if orders else TEXTS["orders_empty"]

        await message.reply(TEXTS["profile_full"].format(user.id, user.stars, orders_text))

    @app.on_callback_query()
    async def callback_handler(client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        user = await get_user_data(user_id)

        if not user and user.role != Roles.ADMIN.value:
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
            await callback_query.answer(TEXTS["unknown_action"], show_alert=True)

    @app.on_message(filters.text and filters.private)
    async def main_handler(client, message):
        user_id = message.from_user.id
        user = await get_user_data(user_id)

        if (user and user.name == "Unknown"):
            await update_data(user_id=user_id, name=message.from_user.first_name or "none", username=message.from_user.username or "none")
        if (user_id not in user_state) or (user_id not in user_data):
            user_state[user_id] = None
            user_data[user_id] = {}

        role = Roles.RECEIVER
        if user:
            role = Roles(user.role)

        text = message.text.strip()
        state = user_state.get(user_id)

        if (role == Roles.RECEIVER):
            return

        try:
            action = ButtonAction(text)
            if action == ButtonAction.RETURN:
                user_state[user_id] = None
                await message.reply(TEXTS["back_to_main"], reply_markup=get_main_menu(role))
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

        await message.reply(TEXTS["not_understood"], reply_markup=get_main_menu(role))
