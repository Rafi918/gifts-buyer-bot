from enum import Enum

class Roles(str, Enum):
    ADMIN = "admin"
    BUYER = "buyer"
    RECEIVER = "receiver"