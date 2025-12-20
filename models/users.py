from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Column
from core.db import Base
from models.collections import cart, favorites

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hash = Column(String(255), nullable=False)

    orders = relationship("Order", back_populates="user")
    cart = relationship("Product", secondary=cart, back_populates="in_cart_user")

    favorites = relationship("Product", secondary=favorites, back_populates="favorited_by_user")