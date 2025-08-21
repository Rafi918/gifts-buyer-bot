from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_crud import get_users, count_users, add_user, update_role, remove_user
from keyboards.reply import get_users_menu, get_role_keyboard, get_return_menu, get_main_menu
from constants.states import States
from constants.button_action import ButtonAction
from constants.roles import Roles
from constants.texts import TEXTS
from logger import logger


def get_users_inline_keyboard(page: int, total_pages: int):
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(
            "⬅ Previous", callback_data=f"prev_{page}"))
    if page + 1 < total_pages:
        nav_buttons.append(InlineKeyboardButton(
            "Next ➡", callback_data=f"next_{page}"))

    if not nav_buttons:
        return None
    return InlineKeyboardMarkup([nav_buttons])


async def update_users_list_page(client, message, page: int):
    limit = 5
    total_users = await count_users()
    total_pages = (total_users + limit - 1) // limit
    users = await get_users(page=page, limit=limit)

    if not users:
        await message.edit_text(TEXTS["no_users_found"])
        return

    user_list = "\n".join(
        [
                f"{i + 1 + (page * limit)}. "
            + (f"<a href='https://t.me/{u.username}'>{u.name}</a> " if u.username and u.username != "none" else u.name)
            + f"({u.role}) – ID: `{u.id}`, Stars: {u.stars}⭐️"
            for i, u in enumerate(users)
        ]
    )
    try:
        await message.edit_text(
            user_list,
            reply_markup=get_users_inline_keyboard(page, total_pages)
        )
    except Exception as e:
        logger.error(f"Error editing message: {e}")


async def handle_users(client, message, state, user_data, role):

    if role != Roles.ADMIN:
        return None

    user_id = message.from_user.id
    text = message.text.strip()
    limit = 5

    page = 0

    if text == ButtonAction.USERS.value:
        total_users = await count_users()
        users = await get_users(page=page, limit=limit)

        if not users:
            await message.reply(TEXTS["dont_hack_me"], reply_markup=get_main_menu(role))
            return None

        user_list = "\n".join(
            [
                    f"{i + 1 + (page * limit)}. "
                    + (f"<a href='https://t.me/{u.username}'>{u.name}</a> " if u.username and u.username != "none" else u.name)
                    + f"({u.role}) – ID: `{u.id}`, Stars: {u.stars}⭐️"
                    for i, u in enumerate(users)
            ]
        )
        total_pages = (total_users + limit - 1) // limit

        await message.reply(
            user_list,
            reply_markup=get_users_inline_keyboard(page, total_pages)
        )
        await message.reply(TEXTS["choose_action"], reply_markup=get_users_menu())
        return States.USERS_MENU

    if text == ButtonAction.ADD_USER.value:
        await message.reply(TEXTS["ask_user_id_add"],
                            reply_markup=get_return_menu())
        return States.AWAITING_USER_ID_FOR_ADD

    if state == States.AWAITING_USER_ID_FOR_ADD:
        if not text.isdigit():
            await message.reply(TEXTS["invalid_user_id"],
                                reply_markup=get_return_menu())
            return States.AWAITING_USER_ID_FOR_ADD

        try:
            tg_user = await client.get_users(int(text))
            name = tg_user.first_name or "NoName"
            username = tg_user.username or None
        except Exception:
            name = "Unknown"
            username = None

        await add_user(user_id=int(text), name=name, username=username)

        await message.reply(TEXTS["user_added"].format(text), reply_markup=get_users_menu())
        return States.USERS_MENU

    if text == ButtonAction.REMOVE_USER.value:
        await message.reply(TEXTS["ask_user_id_remove"],
                            reply_markup=get_return_menu())
        return States.AWAITING_USER_ID_FOR_REMOVE

    if state == States.AWAITING_USER_ID_FOR_REMOVE:
        if not text.isdigit():
            await message.reply(TEXTS["invalid_user_id"],
                                reply_markup=get_return_menu())
            return States.AWAITING_USER_ID_FOR_REMOVE

        removed = await remove_user(int(text))
        if removed:
            await message.reply(TEXTS["user_removed"].format(text), reply_markup=get_users_menu())
        else:
            await message.reply(TEXTS["user_not_found"].format(text), reply_markup=get_users_menu())
        return States.USERS_MENU

    if text == ButtonAction.CHANGE_ROLE.value:
        await message.reply(TEXTS["ask_user_id_role"],
                            reply_markup=get_return_menu())
        return States.AWAITING_USER_ID_FOR_ROLE

    if state == States.AWAITING_USER_ID_FOR_ROLE:
        if text.isdigit():
            user_data[user_id]["target_user_id"] = text
            await message.reply(TEXTS["choose_new_role"], reply_markup=get_role_keyboard())
            return States.AWAITING_NEW_ROLE
        else:
            await message.reply(TEXTS["invalid_user_id"],
                                reply_markup=get_return_menu())
            return States.AWAITING_USER_ID_FOR_ROLE

    if state == States.AWAITING_NEW_ROLE:
        if text in Roles.values():
            target_id = user_data[user_id]["target_user_id"]
            await update_role(target_id, text)
            await message.reply(TEXTS["user_role_updated"].format(target_id, text),
                                reply_markup=get_users_menu())
            return States.USERS_MENU
        else:
            await message.reply(TEXTS["invalid_role"],
                                reply_markup=get_role_keyboard())
            return States.AWAITING_NEW_ROLE

    return state
