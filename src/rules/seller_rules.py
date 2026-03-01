from enum import Enum
from models.users import Seller

class SellerStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"

def can_interact_product(seller: Seller):
    return seller.status == SellerStatus.ACTIVE