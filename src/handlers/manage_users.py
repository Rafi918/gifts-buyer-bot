from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_crud import get_users, count_users, add_user, update_role, remove_user
from keyboards.reply import get_users_menu, get_role_keyboard, get_return_menu, get_main_menu
from constants.states import States
from constants.button_action import ButtonAction


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
    limit = 2
    total_users = await count_users()
    total_pages = (total_users + limit - 1) // limit
    users = await get_users(page=page, limit=limit)

    if not users:
        await message.edit_text("⚠ No users found.")
        return

    user_list = "\n".join(
        [f"{i + 1 + (page * limit)}. {u.name} ({u.role}) – ID: `{u.id}` \n"
         for i, u in enumerate(users)]
    )

    try:
        await message.edit_text(
            f"📋 Users:\n\n{user_list}\n\n📄 Page {page + 1} of {total_pages}",
            reply_markup=get_users_inline_keyboard(page, total_pages)
        )
    except Exception as e:
        print("Error editing message:", e)


async def handle_users(client, message, state, user_data, role):

    if (role != "admin"):
        return

    user_id = message.from_user.id
    text = message.text.strip()
    limit = 2

    page = 0

    if text == ButtonAction.USERS.value:
        total_users = await count_users()
        users = await get_users(page=page, limit=limit)

        if not users:
            await message.reply("Don't Hack me, Please", reply_markup=get_main_menu(role))
            return None

        user_list = "\n".join(
            [f"{i + 1 + (page * limit)}. {u.name} ({u.role}) – ID: `{u.id}` \n" for i,
             u in enumerate(users)]
        )

        total_pages = (total_users + limit - 1) // limit

        await message.reply(
            f"📋 Users:\n\n{user_list}\n\n📄 Page {page + 1} of {total_pages}",
            reply_markup=get_users_inline_keyboard(page, total_pages)
        )
        await message.reply("Choose an action:", reply_markup=get_users_menu())
        return States.USERS_MENU

    if text == ButtonAction.ADD_USER.value:
        await message.reply("Please send the **Telegram user_id** of the user you want to add:",
                            reply_markup=get_return_menu())
        return States.AWAITING_USER_ID_FOR_ADD

    if state == States.AWAITING_USER_ID_FOR_ADD:
        if not text.isdigit():
            await message.reply("❌ Invalid user ID. Please send a numeric user_id.",
                                reply_markup=get_return_menu())
            return States.AWAITING_USER_ID_FOR_ADD

        try:
            tg_user = await client.get_users(int(text))
            name = tg_user.first_name or "NoName"
            username = tg_user.username or None
        except Exception:
            name = "Unknown"
            username = None

        await add_user(user_id=int(text), name=name, username=username, role="receiver")

        await message.reply(f"✅ User {text} added as receiver.", reply_markup=get_users_menu())
        return States.USERS_MENU

    # 🗑 REMOVE USER FLOW
    if text == ButtonAction.REMOVE_USER.value:
        await message.reply("Please send the **Telegram user_id** of the user you want to remove:",
                            reply_markup=get_return_menu())
        return States.AWAITING_USER_ID_FOR_REMOVE

    if state == States.AWAITING_USER_ID_FOR_REMOVE:
        if not text.isdigit():
            await message.reply("❌ Invalid user ID. Please send a numeric user_id.",
                                reply_markup=get_return_menu())
            return States.AWAITING_USER_ID_FOR_REMOVE

        removed = await remove_user(int(text))
        if removed:
            await message.reply(f"✅ User {text} removed.", reply_markup=get_users_menu())
        else:
            await message.reply(f"❌ User {text} not found.", reply_markup=get_users_menu())
        return States.USERS_MENU

    if text == ButtonAction.CHANGE_ROLE.value:
        await message.reply("Please send the **Telegram user_id** of the user whose role you want to change:",
                            reply_markup=get_return_menu())
        return States.AWAITING_USER_ID_FOR_ROLE

    if state == States.AWAITING_USER_ID_FOR_ROLE:
        if text.isdigit():
            user_data[user_id]["target_user_id"] = int(text)
            await message.reply("Choose the new role:", reply_markup=get_role_keyboard())
            return States.AWAITING_NEW_ROLE
        else:
            await message.reply("❌ Invalid user ID. Please send a numeric user_id.",
                                reply_markup=get_return_menu())
            return States.AWAITING_USER_ID_FOR_ROLE

    if state == States.AWAITING_NEW_ROLE:
        if text in ["admin", "buyer", "receiver"]:
            target_id = user_data[user_id]["target_user_id"]
            await update_role(target_id, text)
            await message.reply(f"✅ User {target_id} is now a **{text}**.",
                                reply_markup=get_users_menu())
            return States.USERS_MENU
        else:
            await message.reply("❌ Invalid role. Choose: admin / buyer / receiver",
                                reply_markup=get_role_keyboard())
            return States.AWAITING_NEW_ROLE

    return state
