from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Boolean, Column, DateTime, func

from core.db import Base
from models import cart, favorites

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    email_verified = Column(Boolean, default=False)
    hashed_password = Column(String(255), nullable=False)
    avatar = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=func.now())

    email_token = relationship("EmailToken", back_populates="user", uselist=False)
    tokens = relationship("RefreshToken", back_populates="user")
    orders = relationship("Order", back_populates="user")
    cart_products = relationship("Product", secondary=cart, back_populates="in_cart_user")
    favorite_products = relationship("Product", secondary=favorites, back_populates="favorited_by_user")