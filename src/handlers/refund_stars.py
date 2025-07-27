from keyboards.reply import get_return_menu, get_main_menu
from database.users_crud import get_user_data, update_user_stars
from constants.texts import TEXTS
from constants.states import States
from pyrogram.raw.functions.payments import RefundStarsCharge
from pyrogram.raw.types import InputPeerSelf, InputStarsTransaction


async def handle_refund_stars(client, message, state, user_data, role):
    user_id = message.from_user.id
    text = message.text.strip()

    if state is None:
        await message.reply(TEXTS["refund_request"], reply_markup=get_return_menu())
        return States.AWAITING_REFUND_ID

    elif state == States.AWAITING_REFUND_ID:
        try:
            tids = [InputStarsTransaction(id=text)]
            peer = InputPeerSelf()
            # result = await client.invoke(
            #     GetStarsTransactionsByID(peer=peer, id=tids)
            # )
            # print("found", result)
            # response = await client.refund_star_payment(
            #     user_id=user_id,
            #     telegram_payment_charge_id=text
            # )

            result = await client.invoke(
                RefundStarsCharge(user_id=user_id, charge_id=text)
            )
            print("found", result)

            # if not response:
            #     print("refund", response)
            #     await message.reply(f"❌ Refund failed", reply_markup=get_main_menu(role))

            # user = get_user_data(user_id)
            # updated_stars = user.stars + query.total_amount
            # client.getStarsTransactionsByID

            # await update_user_stars(user_id, updated_stars)

        except Exception as e:
            await message.reply(f"❌ Error while refunding: {str(e)}", reply_markup=get_main_menu(role))

        return None

    return state
