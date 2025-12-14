from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core.db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hash: Mapped[str] = mapped_column(String(255), nullable=False)