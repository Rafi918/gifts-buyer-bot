from handlers.charge_stars import handle_charge_stars
from handlers.refund_stars import handle_refund_stars
from handlers.orders import handle_orders
from handlers.send_gift import handle_send_gift
from handlers.manage_users import handle_users
from constants.states import States

STATE_HANDLERS = {
    States.AWAITING_STAR_AMOUNT: handle_charge_stars,
    States.CONFIRMING_STAR_CHARGE: handle_charge_stars,
    States.AWAITING_REFUND_ID: handle_refund_stars,
    States.ADDING_ORDER: handle_orders,
    States.CONFIRMING_ORDER: handle_orders,
    States.REMOVING_ORDER: handle_orders,
    States.AWAITING_GIFT_ID: handle_send_gift,
    States.USERS_MENU: handle_users,
    States.AWAITING_USER_ID_FOR_ROLE: handle_users,
    States.AWAITING_NEW_ROLE: handle_users,
}

BUTTON_HANDLERS = {
    "Charge Stars": handle_charge_stars,
    "Refund Stars": handle_refund_stars,
    "Orders": handle_orders,
    "Add Order": handle_orders,
    "Remove Order": handle_orders,
    "Send Gift": handle_send_gift,
    "Users": handle_users,
    "Add User": handle_users,
    "Remove User": handle_users,
    "Change Role": handle_users,
}
