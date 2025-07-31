from enum import Enum


class Roles(str, Enum):
    ADMIN = "admin"
    BUYER = "buyer"
    RECEIVER = "receiver"

    @classmethod
    def values(cls):
        return [role.value for role in cls]
