from keyboards.reply import get_return_menu, get_main_menu
from constants.texts import TEXTS
from constants.states import States
from database.users_crud import get_user, deduct_user_stars
from logger import logger


async def handle_send_gift(client, message, state, user_data, role):
    user_id = message.from_user.id
    user = await get_user(user_id)

    if not user or user.stars < 15:
        await message.reply(TEXTS["not_enough_stars"], reply_markup=get_main_menu(role))
        return None

    if state is None:

        await message.reply(TEXTS["sending_gift_prompt_testing"], reply_markup=get_return_menu())
        return States.AWAITING_USER_ID_SENDING_GIFT

    elif state == States.AWAITING_USER_ID_SENDING_GIFT:
        try:
            receiver_id = message.text.strip()

            await client.send_gift(
                chat_id=receiver_id,
                gift_id=5170233102089322756,
                is_private=True,
            )
            await deduct_user_stars(user_id, 15) 
            await message.reply(TEXTS["gift_sent"], reply_markup=get_main_menu(role))

        except Exception as e:
            logger.error(TEXTS["gift_error"].format(str(e)))
            await message.reply(TEXTS["gift_error"].format(str(e)), reply_markup=get_main_menu(role))

        return None
