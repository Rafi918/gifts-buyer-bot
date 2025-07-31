from keyboards.reply import get_main_menu
from constants.texts import TEXTS
from constants.roles import Roles


async def handle_start(client, message, role):
    if (role == Roles.RECEIVER):
        await message.reply(TEXTS["welcome_receiver"], reply_markup=get_main_menu(role))
        return

    await message.reply(TEXTS["welcome"], reply_markup=get_main_menu(role))
