
from enum import Enum


class States(str, Enum):
    # 🌟 Charging stars
    AWAITING_STAR_AMOUNT = "awaiting_star_amount"
    CONFIRMING_STAR_CHARGE = "confirming_star_charge"

    # 💰 Refunds
    AWAITING_REFUND_ID = "awaiting_refund_id"

    # 📦 Orders
    ADDING_ORDER = "adding_order"
    CONFIRMING_ORDER = "confirming_order"
    REMOVING_ORDER = "removing_order"

    # 🎁 Gifts
    AWAITING_GIFT_ID = "awaiting_gift_id"

    # 👥 Users
    USERS_MENU = "users_menu"
    AWAITING_USER_ID_FOR_ADD = "awaiting_user_id_for_add"
    AWAITING_USER_ID_FOR_REMOVE = "awaiting_user_id_for_remove"
    AWAITING_USER_ID_FOR_ROLE = "awaiting_user_id_for_role"
    AWAITING_NEW_ROLE = "awaiting_new_role"
