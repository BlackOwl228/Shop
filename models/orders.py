from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column, Integer, DateTime, func, Numeric, String
from core.db import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Numeric, nullable=False, default=0)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))

    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Numeric, nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")