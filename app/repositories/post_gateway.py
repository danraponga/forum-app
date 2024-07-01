from typing import List

from sqlalchemy.orm import Session

from app.models.common.status import Status
from app.models.post import Post


class PostDbGateway:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, post: Post) -> None:
        self.db.add(post)
        self.db.commit()

    def get_by_id(self, post_id: int) -> Post:
        return (
            self.db.query(Post)
            .filter(Post.id == post_id, Post.status == Status.ACTIVE)
            .first()
        )

    def get_user_posts(self, user_id: int) -> List[Post]:
        return self.db.query(Post).filter(Post.owner_id == user_id).all()

    def get_list(self, skip: int, limit: int) -> List[Post]:
        return (
            self.db.query(Post)
            .filter(Post.status == Status.ACTIVE)
            .offset(skip)
            .limit(limit)
            .all(),
            self.get_total(),
        )

    def update(self, post: Post, data: dict) -> None:
        allowed_fields = [
            "content",
            "ai_enabled",
            "ai_delay_minutes",
        ]
        for field, value in data.items():
            if field in allowed_fields and value:
                setattr(post, field, value)
        self.db.commit()

    def delete(self, post: Post) -> None:
        self.db.delete(post)
        self.db.commit()

    def get_total(self) -> int:
        return self.db.query(Post).filter(Post.status == Status.ACTIVE).count()
