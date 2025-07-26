from pyrogram.types import ReplyKeyboardMarkup


def get_main_menu():
    return ReplyKeyboardMarkup(
        [["Charge Stars", "Refund Stars"], ["Orders", "Send Gift"]],
        resize_keyboard=True
    )


def get_return_menu():
    return ReplyKeyboardMarkup(
        [["Return"]],
        resize_keyboard=True
    )


def get_confirmation_menu():
    return ReplyKeyboardMarkup(
        [["Yes", "No"], ["Return"]],
        resize_keyboard=True
    )


def get_orders_menu():
    return ReplyKeyboardMarkup(
        [["Add Order", "Remove Order"], ["Return"]],
        resize_keyboard=True
    )


def get_order_remove_keyboard(order_count):
    return ReplyKeyboardMarkup(
        [[str(i + 1) for i in range(order_count)], ["Return"]],
        resize_keyboard=True
    )
