from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from core.db import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    total_price = Column(Numeric(10, 2), nullable=False, default=0)
    status = Column(String, default="pending")
    payment_intent = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    variant_id = Column(ForeignKey("product_variants.id"), nullable=False)

    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="order_items")
    product_variant = relationship("ProductVariant", back_populates="order_items")
