from enum import Enum

class SellerStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"

def can_interact_product(seller):
    return seller.status == SellerStatus.ACTIVE