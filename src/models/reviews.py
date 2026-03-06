from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger, String, func
from sqlalchemy.orm import relationship

from core.db import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(SmallInteger, nullable=False)
    text = Column(String(500), nullable=True)
    image = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=func.now())

    product = relationship("Product", back_populates="reviews")
    author = relationship("User", back_populates="reviews")
