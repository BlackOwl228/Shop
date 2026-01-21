from enum import Enum

class ProductStatus(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"

def can_order_product(product):
    return product.status == ProductStatus.ACTIVE

def can_view_product(product):
    return product.status == ProductStatus.ACTIVE

from models import Product, Seller
from .seller_rules import SellerStatus

def available_products(query):
    return (
    query
    .join(Seller)
    .filter(Product.status == ProductStatus.ACTIVE,
            Product.stock > 0,
            Seller.status == SellerStatus.ACTIVE,
            )
        )