from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.db import Base
from app.models.common.status import Status


class Comment(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    parent_comment_id = Column(Integer, ForeignKey("comment.id"), nullable=True)
    content = Column(String, nullable=False)
    status = Column(Enum(Status), default=Status.ACTIVE)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    children = relationship(
        "Comment",
        backref="parent",
        remote_side=[id],
        cascade="all, delete-orphan",
        single_parent=True,
    )
    owner = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
