from enum import Enum


class ButtonAction(Enum):
    CHARGE_STARS = "Charge Stars"
    REFUND_STARS = "Refund Stars"
    ORDERS = "Orders"
    ADD_ORDER = "Add Order"
    REMOVE_ORDER = "Remove Order"
    SEND_GIFT = "Send Gift"
    USERS = "Users"
    ADD_USER = "Add User"
    REMOVE_USER = "Remove User"
    CHANGE_ROLE = "Change Role"
    RETURN = "Return"

    # Channels
    USER_CHANNELS = "Channels"
    ADD_CHANNEL = "Add Channel"
    REMOVE_CHANNEL = "Remove Channel"

    # Relayers
    RELAYERS = "Relayers"
    ADD_RELAYER = "Add Relayer"
    REMOVE_RELAYER = "Remove Relayer"
