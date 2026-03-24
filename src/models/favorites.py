from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.core.resources.db import Base


class Favorite(Base):
    __tablename__ = "favorites"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="favorites")
    product = relationship("Product", back_populates="in_favorites")
