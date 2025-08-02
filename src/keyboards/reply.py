from pyrogram.types import ReplyKeyboardMarkup
from constants.roles import Roles


def build_keyboard(buttons: list[list[str]]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def get_main_menu(role: Roles) -> ReplyKeyboardMarkup:
    if role == Roles.RECEIVER:
        return None
    elif role == Roles.ADMIN:
        return build_keyboard([
            ["Charge Stars", "Refund Stars"],
            ["Orders", "Send Gift"],
            ["Users"]
        ])
    else:
        return build_keyboard([
            ["Charge Stars", "Refund Stars"],
            ["Orders", "Send Gift"]
        ])


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


def get_users_menu():
    return build_keyboard([
        ["Add User", "Remove User", "Change Role"],
        ["Return"]
    ])


def get_role_keyboard():
    return build_keyboard([
        Roles.values(),
        ["Return"]
    ])
