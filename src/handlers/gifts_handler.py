import re
from pyrogram.types import ReplyKeyboardMarkup, Message
from pyrogram import Client
from database.channels_crud import list_channels
from database.users_crud import get_user
from database.orders_crud import add_order, remove_order
from database.relayers_crud import list_relay_targets
from constants.states import States
from constants.texts import TEXTS
from keyboards.reply import get_return_menu, get_main_menu
from user_bot import user_bot
from logger import logger
from helpers.buy_gift import try_buying_gift


async def handle_buy_gift(client: Client, message: Message, state, user_data, role):
    user_id = message.from_user.id
    text = (message.text or "").strip()

    if state is None and message.reply_to_message:
        replied = message.reply_to_message
        if replied.from_user.is_bot and text.isdigit() and replied.text.endswith("^_^"):

            gift_id = (replied.text.split("\n")[0]).strip("`")
            price_match = re.search(r"Price:\s*(\d+)", replied.text)
            if not price_match:
                await message.reply("❌ Invalid gift message format.")
                return None

            gift = {"id": int(gift_id), "price": int(price_match.group(1))}
            user_data[user_id] = {
                "gift": gift,
                "gift_count": int(text),
                "gift_reply_to": replied.id,
            }

            buttons = [["Yourself"]]
            channels = await list_channels(user_id)
            if channels:
                buttons.append([c.name for c in channels])

            targets = await list_relay_targets(user_id)
            if targets:
                buttons.append(["Friends"])

            buttons.append(["Return"])

            await replied.reply(
                "Choose recipient:",
                reply_markup=ReplyKeyboardMarkup(
                    buttons, resize_keyboard=True),
                quote=True,
            )
            return States.CHOOSING_GIFT_RECIPIENT

    if state == States.CHOOSING_GIFT_RECIPIENT:
        if text == "Friends":
            targets = await list_relay_targets(user_id)
            if not targets:
                await message.reply("❌ You have no friends to relay for.", reply_markup=get_return_menu())
                return States.CHOOSING_GIFT_RECIPIENT

            buttons = [[t.name for t in targets], ["Return"]]
            await message.reply(
                "Select a friend to send the gift to:",
                reply_markup=ReplyKeyboardMarkup(
                    buttons, resize_keyboard=True),
                quote=True,
            )
            return States.CHOOSING_GIFT_RECIPIENT

        recipient_id = user_id if text == "Yourself" else None
        if recipient_id is None:
            target_id = user_data[user_id].get("target_id", user_id)

            print(f"Target ID for relayer: {target_id}")

            channels = await list_channels(target_id)
            match = next((c for c in channels if c.name == text), None)

            if not match:
                targets = await list_relay_targets(user_id)
                match = next((t for t in targets if t.name == text), None)
                if match:
                    user_data[user_id]["target_id"] = match.id
                    buttons = [[text]]
                    channels = await list_channels(match.id)
                    if channels:
                        buttons.append([c.name for c in channels])

                    buttons.append(["Return"])

                    await message.reply(
                        "Choose recipient:",
                        reply_markup=ReplyKeyboardMarkup(
                            buttons, resize_keyboard=True),
                        quote=True,
                    )
                    return States.CHOOSING_GIFT_RECIPIENT

            if not match:
                await message.reply("❌ Invalid choice. Try again.", reply_markup=get_return_menu())
                return States.CHOOSING_GIFT_RECIPIENT

            recipient_id = match.id

        user_data[user_id]["recipient_id"] = recipient_id

        reply_to_id = user_data[user_id]["gift_reply_to"]
        gift_count = user_data[user_id]["gift_count"]
        recipient = await get_user(recipient_id)
        recipient_label = (
            TEXTS["user_link"].format(
                username=recipient.username, name=recipient.name)
            if recipient.username and recipient.username != "none"
            else recipient.name
        ) + f", ID:{recipient.id}"

        await message.reply(
            f"Confirm purchase:\n\n Gift Count: {gift_count} \n Recipient: {recipient_label}",
            reply_markup=ReplyKeyboardMarkup(
                [["Yes", "No"]], resize_keyboard=True),
            reply_to_message_id=reply_to_id,
            quote=True,
        )
        return States.CONFIRMING_GIFT_PURCHASE

    if state == States.CONFIRMING_GIFT_PURCHASE:
        if text == "Yes":
            gift = dict(user_data[user_id]["gift"])
            gift_count = user_data[user_id]["gift_count"]
            recipient_id = user_data[user_id]["recipient_id"]
            reply_to_id = user_data[user_id]["gift_reply_to"]
            target_id = user_data[user_id].get("target_id", user_id)

            try:
                user_bot_data = await user_bot.get_me()
                result, order = await add_order(
                    target_id, -1, -1, -1, -1, gift_count, recipient_id
                )
                order.user = await get_user(target_id)

                if result:
                    for _ in range(gift_count):
                        tmp_order = await try_buying_gift(
                            app=client, user_bot=user_bot, gift=gift,
                            order=order, user_bot_id=user_bot_data.id
                        )
                        if not tmp_order:
                            raise Exception("You can't buy this gift.")
                        order = tmp_order

                await remove_order(target_id, order.id)
                await client.send_message(
                    chat_id=message.chat.id,
                    text=f"🎉 You bought {gift_count}x Gift `{gift['id']}` for {recipient_id}!",
                    reply_to_message_id=reply_to_id,
                    reply_markup=get_main_menu(role),
                )
            except Exception as e:
                if (order.completed_count > 0):
                    await client.send_message(
                        chat_id=message.chat.id,
                        text=f"🎉 You bought {order.completed_count}x Gift `{gift['id']}` for {recipient_id}!",
                        reply_to_message_id=reply_to_id,
                        reply_markup=get_main_menu(role),
                    )
                await remove_order(target_id, order.id)
                await message.reply(
                    f"❌ Error sending gift: {e}", reply_markup=get_main_menu(role)
                )
                logger.error(
                    f"Error sending gift {gift['id']} to {recipient_id}: {e}")

            user_data.pop(user_id, None)
            return None

        if text == "No":
            await message.reply("Purchase cancelled.", reply_markup=get_main_menu(role))
            user_data.pop(user_id, None)
            return None

        return States.CONFIRMING_GIFT_PURCHASE

    return state
