from enum import StrEnum

from models.users import Seller


class SellerStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"


def can_interact_product(seller: Seller):
    return seller.status == SellerStatus.ACTIVE
