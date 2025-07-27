from keyboards.reply import get_main_menu
from constants.texts import TEXTS

async def handle_start(client, message,role):
    await message.reply(TEXTS["welcome"], reply_markup=get_main_menu(role))