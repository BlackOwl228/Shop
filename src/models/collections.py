from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from core.db import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    # parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True) #идея на будущее

    # children = relationship("Category")
    products = relationship("Product", back_populates="category")


class CartItem(Base):
    __tablename__ = "cart_items"

    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    variant_id = Column(ForeignKey("product_variants.id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer, default=1, nullable=False)

    user = relationship("User", back_populates="cart_items")
    variant = relationship("ProductVariant", back_populates="cart_items")


favorites = Table(
    "favorites",
    Base.metadata,
    Column("user", Integer, ForeignKey("users.id"), primary_key=True),
    Column("product", Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
)
