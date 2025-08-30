from database.relayers_crud import (
    list_relayers,
    add_relayer,
    remove_relayer,
)
from constants.texts import TEXTS
from constants.states import States
from constants.button_action import ButtonAction
from keyboards.reply import get_relayers_menu, get_return_menu, get_main_menu


async def handle_relayers(client, message, state, user_data, role):
    user_id = message.from_user.id
    username = message.from_user.username
    text = (message.text or "").strip()

    if state == States.AWAITING_RELAYER_ID_FOR_ADD:
        if text.isdigit() and int(text) == user_id or username == text.lstrip("@"):
            await message.reply(TEXTS["you_are_the_relayer"], reply_markup=get_return_menu())
            return States.AWAITING_RELAYER_ID_FOR_ADD
        ok, info = await add_relayer(user_id, text)
        if ok:
            await message.reply(TEXTS["relayer_added"].format(info), reply_markup=get_main_menu(role))
            return States.RELAYERS_MENU

        if info == "exists":
            await message.reply(TEXTS["relayer_already_added"].format(text), reply_markup=get_return_menu())
        else:
            await message.reply(TEXTS["relayer_not_found"].format(text), reply_markup=get_return_menu())
        return States.AWAITING_RELAYER_ID_FOR_ADD

    if state == States.AWAITING_RELAYER_ID_FOR_REMOVE:
        ok, info = await remove_relayer(user_id, text)
        if ok:
            await message.reply(TEXTS["relayer_removed"].format(info), reply_markup=get_relayers_menu())
            return States.RELAYERS_MENU
        else:
            await message.reply(TEXTS["relayer_not_found"].format(text), reply_markup=get_return_menu())
            return States.AWAITING_RELAYER_ID_FOR_REMOVE

    if text == ButtonAction.ADD_RELAYER.value:
        await message.reply(TEXTS["relayers_ask_id"], reply_markup=get_return_menu())
        return States.AWAITING_RELAYER_ID_FOR_ADD

    if text == ButtonAction.REMOVE_RELAYER.value:
        await message.reply(
            TEXTS["relayers_ask_id"], reply_markup=get_return_menu())
        return States.AWAITING_RELAYER_ID_FOR_REMOVE

    if text == ButtonAction.RELAYERS.value or state is None or state == States.RELAYERS_MENU:
        relayers = await list_relayers(user_id)
        if not relayers:
            await message.reply(TEXTS["relayers_empty"], reply_markup=get_relayers_menu())
        else:

            relayer_list = "\n".join(
                [TEXTS["relayers_list_item"].format(
                    (TEXTS["user_link"].format(
                        username=user.username, name=user.name)
                        if user.username and user.username != "none"
                        else user.name
                     ), user.id) for user in relayers]
            )
            await message.reply(
                TEXTS["relayers_menu_title"].format(relayer_list),
                reply_markup=get_relayers_menu(),
            )
        return States.RELAYERS_MENU

    return state
