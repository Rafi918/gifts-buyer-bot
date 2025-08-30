from database.channels_crud import list_channels, add_channel, remove_channel
from constants.texts import TEXTS
from constants.states import States
from constants.button_action import ButtonAction
from keyboards.reply import get_channels_menu, get_return_menu, get_main_menu


async def handle_channels(client, message, state, user_data, role):
    user_id = message.from_user.id
    text = (message.text or "").strip()

    if state == States.AWAITING_CHANNEL_ID_FOR_ADD:
        ok, info = await add_channel(user_id, text)
        if ok:
            await message.reply(TEXTS["channels_added"].format(info), reply_markup=get_main_menu(role))
            return States.CHANNELS_MENU

        if info == "limit":
            await message.reply(TEXTS["channels_limit_reached"], reply_markup=get_channels_menu())
            return States.CHANNELS_MENU

        if info == "exists":
            await message.reply(TEXTS["channels_already_added"].format(text), reply_markup=get_main_menu(role))
            return States.CHANNELS_MENU

        await message.reply(TEXTS["channels_not_found"].format(text), reply_markup=get_return_menu())
        return States.AWAITING_CHANNEL_ID_FOR_ADD

    if state == States.AWAITING_CHANNEL_ID_FOR_REMOVE:
        ok, info = await remove_channel(user_id, text)
        if ok:
            await message.reply(TEXTS["channels_removed"].format(info), reply_markup=get_channels_menu())
            return States.CHANNELS_MENU
        else:
            await message.reply(TEXTS["channels_not_found"].format(text), reply_markup=get_return_menu())
            return States.AWAITING_CHANNEL_ID_FOR_REMOVE

    if text == ButtonAction.ADD_CHANNEL.value:
        await message.reply(TEXTS["channels_ask_id"], reply_markup=get_return_menu())
        return States.AWAITING_CHANNEL_ID_FOR_ADD

    if text == ButtonAction.REMOVE_CHANNEL.value:
        channels = await list_channels(user_id)
        if not channels:
            await message.reply(TEXTS["channels_empty"], reply_markup=get_channels_menu())
            return States.CHANNELS_MENU

        await message.reply(TEXTS["channels_ask_id"], reply_markup=get_return_menu())
        return States.AWAITING_CHANNEL_ID_FOR_REMOVE

    if text == ButtonAction.USER_CHANNELS.value or state is None or state == States.CHANNELS_MENU:
        channels = await list_channels(user_id)
        if not channels:
            await message.reply(TEXTS["channels_empty"], reply_markup=get_channels_menu())
        else:
            channel_list = "\n".join(
                TEXTS["channels_list_item"].format(
                    (f"<a href='https://t.me/{c.username}'>{c.name}</a>"
                     if c.username and c.username != "none" else c.name),
                    c.id
                )
                for c in channels
            )
            await message.reply(TEXTS["channels_menu_title"].format(channel_list), reply_markup=get_channels_menu())
        return States.CHANNELS_MENU

    return state
