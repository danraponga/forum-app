from typing import List
from sqlalchemy import  ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base
from app.models.common.enums.status import Status
from app.models.common.timestamped import TimestampedModel

class Post(Base, TimestampedModel):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[Status] = mapped_column(default=Status.ACTIVE)
    ai_enabled: Mapped[bool] = mapped_column(default=False)
    ai_delay_minutes: Mapped[int] = mapped_column(default=5)

    owner: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )
