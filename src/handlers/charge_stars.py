from keyboards.reply import get_return_menu, get_main_menu
from constants.texts import TEXTS
from pyrogram.types import LabeledPrice
from constants.states import States


async def handle_charge_stars(client, message, state, user_data, role):
    user_id = message.from_user.id
    text = message.text

    # Step 1: Ask for star amount
    if state is None:
        await message.reply(TEXTS["ask_star_amount"], reply_markup=get_return_menu())
        return States.AWAITING_STAR_AMOUNT

    # Step 2: Process star amount and send invoice immediately
    elif state == States.AWAITING_STAR_AMOUNT:
        if not text.isdigit():
            await message.reply("❌ Please enter a valid number.")
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
                f"✅ Invoice sent to charge {stars} stars.",
                reply_markup=get_main_menu(role)
            )
        except Exception as e:
            await message.reply(
                f"❌ Failed to send invoice:\n`{str(e)}`",
                reply_markup=get_main_menu(role)
            )

        return None

    return state
