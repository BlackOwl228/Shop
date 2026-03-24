from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.core.resources.db import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    variant_id = Column(ForeignKey("product_variants.id", ondelete="CASCADE"), primary_key=True)
    quantity = Column(Integer, default=1, nullable=False)

    user = relationship("User", back_populates="cart_items")
    variant = relationship("ProductVariant", back_populates="cart_items")
