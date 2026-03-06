from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from core.db import Base
from models.collections import favorites


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    rating = Column(Float, default=0.0, nullable=False)
    reviews_count = Column(Integer, default=0, nullable=False)
    description = Column(Text, nullable=True)
    seller_id = Column(ForeignKey("sellers.id"), nullable=False)
    category_id = Column(ForeignKey("categories.id"))
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=func.now())

    variants = relationship("ProductVariant", back_populates="product")
    category = relationship("Category", back_populates="products")
    seller = relationship("Seller", back_populates="products")
    reviews = relationship("Review", back_populates="product")
    favorited_by_user = relationship("User", secondary=favorites, back_populates="favorite_products")


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    name = Column(String(32), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    image = Column(String(128), nullable=True)

    product = relationship("Product", back_populates="variants")
    order_items = relationship("OrderItem", back_populates="product_variant")
    cart_items = relationship("CartItem", back_populates="variant")

    CheckConstraint("stock >= 0", name="ck_variant_stock_non_negative")

    @property
    def rating(self) -> float:
        return self.product.rating if self.product else 0.0

    @property
    def category_id(self) -> int | None:
        return self.product.category_id if self.product else None

    @property
    def seller_id(self) -> int:
        return self.product.seller_id if self.product else 0
