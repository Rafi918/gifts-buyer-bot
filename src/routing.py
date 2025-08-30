from handlers.charge_stars import handle_charge_stars
from handlers.refund_stars import handle_refund_stars
from handlers.orders import handle_orders
from handlers.send_gift import handle_send_gift
from handlers.manage_users import handle_users
from handlers.manage_channels import handle_channels
from handlers.manage_relayers import handle_relayers
from handlers.gifts_handler import handle_buy_gift
from constants.states import States
from constants.button_action import ButtonAction

STATE_HANDLERS = {
    States.AWAITING_STAR_AMOUNT: handle_charge_stars,
    States.CONFIRMING_STAR_CHARGE: handle_charge_stars,
    States.AWAITING_REFUND_ID: handle_refund_stars,
    States.ADDING_ORDER: handle_orders,
    States.CONFIRMING_ORDER: handle_orders,
    States.REMOVING_ORDER: handle_orders,
    States.AWAITING_USER_ID_SENDING_GIFT: handle_send_gift,
    States.USERS_MENU: handle_users,
    States.AWAITING_USER_ID_FOR_ADD: handle_users,
    States.AWAITING_USER_ID_FOR_REMOVE: handle_users,
    States.AWAITING_USER_ID_FOR_ROLE: handle_users,
    States.AWAITING_NEW_ROLE: handle_users,

    # Channels
    States.CHANNELS_MENU: handle_channels,
    States.AWAITING_CHANNEL_ID_FOR_ADD: handle_channels,
    States.AWAITING_CHANNEL_ID_FOR_REMOVE: handle_channels,


    # Relayers
    States.RELAYERS_MENU: handle_relayers,
    States.AWAITING_RELAYER_ID_FOR_ADD: handle_relayers,
    States.AWAITING_RELAYER_ID_FOR_REMOVE: handle_relayers,


    States.CHOOSING_GIFT_RECIPIENT: handle_buy_gift,
    States.CONFIRMING_GIFT_PURCHASE: handle_buy_gift,
}

BUTTON_HANDLERS = {
    ButtonAction.CHARGE_STARS: handle_charge_stars,
    ButtonAction.REFUND_STARS: handle_refund_stars,
    ButtonAction.ORDERS: handle_orders,
    ButtonAction.ADD_ORDER: handle_orders,
    ButtonAction.REMOVE_ORDER: handle_orders,
    ButtonAction.SEND_GIFT: handle_send_gift,
    ButtonAction.USERS: handle_users,
    ButtonAction.ADD_USER: handle_users,
    ButtonAction.REMOVE_USER: handle_users,
    ButtonAction.CHANGE_ROLE: handle_users,
    ButtonAction.USER_CHANNELS: handle_channels,
    ButtonAction.ADD_CHANNEL: handle_channels,
    ButtonAction.REMOVE_CHANNEL: handle_channels,
    ButtonAction.RELAYERS: handle_relayers,
    ButtonAction.ADD_RELAYER: handle_relayers,
    ButtonAction.REMOVE_RELAYER: handle_relayers,
}
