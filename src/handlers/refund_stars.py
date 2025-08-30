from keyboards.reply import get_return_menu, get_main_menu
from database.users_crud import get_user, deduct_user_stars
from database.transaction_crud import get_transaction, refund_transaction
from constants.texts import TEXTS
from constants.states import States
from database.models import Transaction, User
from logger import logger


async def handle_refund_stars(client, message, state, user_data, role):
    user_id = message.from_user.id
    transaction_id = message.text.strip()

    if state is None:
        await message.reply(TEXTS["refund_request"], reply_markup=get_return_menu())
        return States.AWAITING_REFUND_ID

    elif state == States.AWAITING_REFUND_ID:
        try:

            transaction: Transaction = await get_transaction(transaction_id)
            if (transaction.refund_status):
                await message.reply(
                    TEXTS["refund_already_processed"].format(transaction_id),
                    reply_markup=get_main_menu(role)
                )
                return None

            user_data: User = await get_user(user_id)

            if (not user_data or user_data.stars < transaction.total_amount):
                await message.reply(
                    TEXTS["refund_not_enough_stars"],
                    reply_markup=get_main_menu(role)
                )
                return None

            response = await client.refund_star_payment(
                user_id=user_id,
                telegram_payment_charge_id=transaction_id
            )

            if response:
                await deduct_user_stars(user_id, transaction.total_amount)
                await refund_transaction(transaction_id)
                await message.reply(
                    TEXTS["refund_success"],
                    reply_markup=get_main_menu(role)
                )
            else:
                await message.reply(
                    TEXTS["refund_failed"],
                    reply_markup=get_main_menu(role)
                )

        except Exception as e:
            logger.error(TEXTS["refund_error"].format(str(e)))
            await message.reply(TEXTS["refund_error"].format(str(e)), reply_markup=get_main_menu(role))

        return None

    return state
