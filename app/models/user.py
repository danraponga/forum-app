from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base
from app.models.common.timestamped import TimestampedModel


class User(Base, TimestampedModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="owner")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="owner")
