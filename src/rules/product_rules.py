from enum import Enum
from models.products import Product, ProductVariant
from models.users import Seller
from .seller_rules import SellerStatus

class ProductStatus(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    DELETED = "deleted"

def can_order_product(product: Product):
    return product.status == ProductStatus.ACTIVE

def can_view_product(product: Product):
    return product.status == ProductStatus.ACTIVE

def available_products(query):
    return (
    query
    .join(Product)
    .join(Seller)
    .filter(Product.status == ProductStatus.ACTIVE,
            ProductVariant.stock > 0,
            Seller.status == SellerStatus.ACTIVE,
            )
        )