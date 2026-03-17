from sqlalchemy.orm import Session

from src.core.logs.exceptions import (
    CategoryNotFoundError,
    OrderNotFoundError,
    ProductNotFoundError,
    ReviewNotFoundError,
    SellerNotFoundError,
)
from src.models.collections import Category
from src.models.orders import Order
from src.models.products import Product
from src.models.reviews import Review
from src.models.users import Seller, User
from src.rules.order_rules import OrderStatus
from src.rules.product_rules import ProductStatus
from src.rules.seller_rules import SellerStatus


class AdminService:
    def __init__(self, db: Session, admin: User):
        self.db = db
        self.admin = admin

    def product_by_id(self, product_id: int):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ProductNotFoundError(product_id=product_id)

        return product

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

    def seller_by_id(self, seller_id):
        seller = self.db.query(Seller).filter(Seller.id == seller_id).first()
        if not seller:
            raise SellerNotFoundError(seller_id=seller_id)

        return seller

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

    def order_by_id(self, order_id: int):
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise OrderNotFoundError(order_id=order_id)
        return order

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

    def review_by_id(self, review_id: int):
        review = self.db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise ReviewNotFoundError(review_id=review_id)
        return review

    def delete_review(self, review: Review):
        self.db.delete(review)
        self.db.commit()

    def create_category(self, name: str):
        self.db.add(Category(name=name))
        self.db.commit()

    def product_to_category(self, product: Product, category_id: int):
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise CategoryNotFoundError(category_id=category_id)

        product.category_id = category.id
        self.db.commit()
