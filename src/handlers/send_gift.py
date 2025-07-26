from keyboards.reply import get_return_menu, get_main_menu


async def handle_send_gift(client, message, state, user_data):
    user_id = message.from_user.id
    text = message.text.strip()

    if state is None:
        await message.reply("🎁 Please enter your Gift ID to redeem it:", reply_markup=get_return_menu())
        return "awaiting_gift_id"

    elif state == "awaiting_gift_id":
        gift_id = int(text)

        try:
            response = await client.send_gift(
                chat_id=user_id,
                gift_id=gift_id
            )

            if response:
                await message.reply(
                    f"✅ Gift redeemed! ",
                    reply_markup=get_main_menu()
                )
            else:
                print("send gift", response)
                await message.reply(
                    f"❌ Failed to redeem gift",
                    reply_markup=get_main_menu()
                )

        except Exception as e:
            await message.reply(f"❌ Error while redeeming gift:\n`{str(e)}`", reply_markup=get_main_menu())

        return None
