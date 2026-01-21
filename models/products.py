from sqlalchemy.orm import relationship
from sqlalchemy import String, Text, ForeignKey, Numeric, Integer, Float, Column, DateTime, func

from core.db import Base
from models import cart, favorites

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0)
    rating = Column(Float, default=0.0, nullable=False)
    description = Column(Text, nullable=True)
    image = Column(String(128), nullable=True)
    seller_id = Column(ForeignKey("sellers.id"), nullable=False)
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=func.now())

    seller = relationship("Seller")
    order_items = relationship("OrderItem", back_populates="product")
    
    in_cart_user = relationship("User", secondary=cart, back_populates="cart_products")
    favorited_by_user = relationship("User", secondary=favorites, back_populates="favorite_products")