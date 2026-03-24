from sqlalchemy.orm import Session

from src.models.category import Category
from src.models.orders import Order
from src.models.products import Product
from src.models.reviews import Review
from src.models.users import Seller
from src.rules.order_rules import OrderStatus
from src.rules.product_rules import ProductStatus
from src.rules.seller_rules import SellerStatus


class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def block_product(self, product: Product):
        if product.status == ProductStatus.BLOCKED:
            return {"status": "Already blocked"}
        product.status = ProductStatus.BLOCKED
        self.db.commit()

    def unblock_product(self, product: Product):
        if product.status == ProductStatus.ACTIVE:
            return {"status": "Already unblocked"}
        product.status = ProductStatus.ACTIVE
        self.db.commit()

    def approve_seller(self, seller: Seller):
        if seller.status == SellerStatus.ACTIVE:
            return {"status": "Already approved"}
        seller.status = SellerStatus.ACTIVE
        self.db.commit()

    def suspend_seller(self, seller: Seller):
        if seller.status == SellerStatus.SUSPENDED:
            return {"status": "Already suspended"}
        seller.status = SellerStatus.SUSPENDED
        self.db.commit()

    def complete_order(self, order: Order):
        if order.status != OrderStatus.PAID:
            return {"status": "Order not paid yet, you cannot complete it"}
        order.status = OrderStatus.COMPLETED
        self.db.commit()

    def cancel_order(self, order: Order):
        if order.status == OrderStatus.PAID:
            return {"status": "Order already paid you cannot cancel it"}
        order.status = OrderStatus.CANCELLED
        self.db.commit()

    def delete_review(self, review: Review):
        self.db.delete(review)
        self.db.commit()

    def create_category(self, name: str):
        self.db.add(Category(name=name))
        self.db.commit()

    def product_to_category(self, product: Product, category: Category):
        product.category_id = category.id
        self.db.commit()
