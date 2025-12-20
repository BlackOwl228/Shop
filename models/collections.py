from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Column, Table, ForeignKey
from core.db import Base

cart = Table(
    "cart",
    Base.metadata,
    Column("user", Integer, ForeignKey("users.id"), primary_key=True),
    Column("product", Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("quantity", Integer, default=1)
    )

favorites = Table(
    "favorites",
    Base.metadata,
    Column("user", Integer, ForeignKey("users.id"), primary_key=True),
    Column("product", Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)
    )