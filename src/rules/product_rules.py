from enum import Enum
from models.products import Product

class ProductStatus(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"

def can_order_product(product: Product):
    return product.status == ProductStatus.ACTIVE

def can_view_product(product: Product):
    return product.status == ProductStatus.ACTIVE

from models import Product, ProductVariant, Seller
from .seller_rules import SellerStatus

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