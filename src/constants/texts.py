TEXTS = {
    # welcome texts
    "welcome": "Welcome to the Nini Bot! ⭐️ Choose an option:",
    "welcome_receiver": "Welcome to the Nini Bot! ⭐️ You are registered as a receiver.",


    # charging stars texts
    "ask_star_amount": "Please enter the number of stars you'd like to charge:",
    "confirm_star_charge": "Do you want to charge {} stars?",
    "invalid_star_amount": "❌ Please enter a valid number.",
    "invoice_sent": "✅ Invoice sent to charge {} stars.",
    "invoice_failed": "❌ Failed to send invoice:\n`{}`",

    # refund stars texts
    "refund_request": "Please send your transaction ID for the refund.",
    "refund_already_processed": "❌ Refund for transaction {} has already been processed.",
    "refund_not_enough_stars": "❌ You do not have enough stars to refund this transaction.",
    "refund_success": "✅ Refund request sent successfully!",
    "refund_failed": "❌ Failed to send refund request.",
    "refund_error": "❌ Error while refunding: {}",

    # Orders texts
    "orders_empty": "📭 You have no orders yet.",
    "orders_list": "📦 Your orders:\n \n{}",
    "add_order_format": "Please send your order like this:\n `(min stars) (max stars) (min supply) (max supply) (count) (receiver id)` \n \n ex: 2000 5000 0 500000 3 7056348541 ",
    "add_order_confirm": "Do you want to add this order?\n\n<b>Stars</b>: {}-{}⭐️\n<b>Supply</b>: {}-{}\n<b>Receiver</b>: {}, <b>ID</b>: `{}`\n<b>Count</b>: {}",
    "invalid_format": "❌ Invalid format. Please try again.",
    "user_not_found": "❌ User with ID {} not found.",
    "order_added": "✅ Order added.",
    "order_cancelled": "❌ Order cancelled. Enter a new order:",
    "order_confirm_prompt": "Please confirm with 'Yes' or 'No'.",
    "order_removed": "✅ Order removed.",
    "invalid_order_number": "❌ Invalid order number.",
    "max_orders_reached": "🚨 You’ve reached the maximum number of orders. To add a new one, please remove an existing order first.",
    "remove_order_prompt": "📦 Your current orders:\n{}\n\n🗑️ Send the number of the order you want to remove:",

    # app.py texts
    "back_to_main": "🔙 Back to main menu.",
    "profile_user": "Your User ID: `{}`",
    "profile_full": "Your Profile:\n\tUser ID: `{}`\n\tStars: {}⭐️\n\n{}",
    "unknown_action": "Unknown action.",
    "not_understood": "I didn’t understand that. Please use the menu.",
    "adding_channel": "You have added the channel with ID `{}`. Now you send gift to this channel.",
    "channel_already_added": "This channel is already added with ID `{}`.",

    # User management texts
    "no_users_found": "⚠ No users found.",
    "dont_hack_me": "Don't hack me, Please",
    "choose_action": "Choose an action:",
    "ask_user_id_add": "Please send the **Telegram user_id** of the user you want to add:",
    "invalid_user_id": "❌ Invalid user ID. Please send a numeric user_id.",
    "user_added": "✅ User {} added as receiver.",
    "ask_user_id_remove": "Please send the **Telegram user_id** of the user you want to remove:",
    "user_removed": "✅ User {} removed.",
    "user_not_found": "❌ User {} not found.",
    "ask_user_id_role": "Please send the **Telegram user_id** of the user whose role you want to change:",
    "choose_new_role": "Choose the new role:",
    "user_role_updated": "✅ User {} is now a **{}**.",
    "invalid_role": "❌ Invalid role. Choose: admin / buyer / receiver",

    # Sending gifts texts
    "sending_gift_prompt_testing": "🎁 Please enter the **Receiver ID** to send a 🧸 gift. _(Testing only)_",
    "not_enough_stars": "❌ You need at least 15⭐️ to send a 🧸 gift. _(Testing only)_",
    "gift_sent": "✅ Gift sent successfully!",
    "gift_error": "❌ Error while sending gift:\n`{}`"
}
