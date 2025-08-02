from keyboards.reply import get_return_menu, get_main_menu
from constants.texts import TEXTS
from pyrogram.types import LabeledPrice
from constants.states import States


async def handle_charge_stars(client, message, state, user_data, role):
    user_id = message.from_user.id
    text = message.text

    if state is None:
        await message.reply(TEXTS["ask_star_amount"], reply_markup=get_return_menu())
        return States.AWAITING_STAR_AMOUNT

    elif state == States.AWAITING_STAR_AMOUNT:
        if not text.isdigit():
            await message.reply(TEXTS["invalid_star_amount"])
            return States.AWAITING_STAR_AMOUNT

        stars = int(text)

        try:
            check = await client.send_invoice(
                chat_id=user_id,
                title=f"Purchase",
                description=f"Charging {stars} Stars",
                payload="star_charge",
                provider_token="",  # Leave empty for Stars
                currency="XTR",
                prices=[LabeledPrice(label=f"{stars} Stars", amount=stars)],
                start_parameter="star_charge"
            )
            await message.reply(
                TEXTS["invoice_sent"].format(stars),
                reply_markup=get_main_menu(role)
            )
        except Exception as e:
            await message.reply(
                TEXTS["invoice_failed"].format(str(e)),
                reply_markup=get_main_menu(role)
            )

        return None

    return state
