from keyboards.reply import get_return_menu, get_main_menu
from constants.texts import TEXTS


async def handle_refund_stars(client, message, state, user_data):
    user_id = message.from_user.id
    text = message.text.strip()

    if state is None:
        await message.reply(TEXTS["refund_request"], reply_markup=get_return_menu())
        return "awaiting_refund_id"

    elif state == "awaiting_refund_id":
        try:
            response = await client.refund_star_payment(
                user_id=user_id,
                telegram_payment_charge_id=text
            )

            if not response:
                print("refund", response)
                await message.reply(f"❌ Refund failed", reply_markup=get_main_menu())

        except Exception as e:
            await message.reply(f"❌ Error while refunding: {str(e)}", reply_markup=get_main_menu())

        return None

    return state
