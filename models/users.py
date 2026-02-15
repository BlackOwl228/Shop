from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Boolean, Column, DateTime, ForeignKey, func

from core.db import Base
from models import favorites

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    email_verified = Column(Boolean, default=False)
    hashed_password = Column(String(255), nullable=False)
    avatar = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=func.now())
    is_admin = Column(Boolean, default=False)

    email_token = relationship("EmailToken", back_populates="user", uselist=False)
    tokens = relationship("RefreshToken", back_populates="user")
    orders = relationship("Order", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")
    favorite_products = relationship("Product", secondary=favorites, back_populates="favorited_by_user")
    reviews = relationship("Review", back_populates="author")

    seller = relationship("Seller", back_populates="user", uselist=False)

class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    company_name = Column(String(128), nullable=False)
    status = Column(String(20), default="pending")

    created_at = Column(DateTime, default=func.now())
    verified_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="seller")
    products = relationship("Product", back_populates="seller")