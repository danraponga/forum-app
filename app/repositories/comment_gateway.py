from datetime import datetime
from typing import List, Tuple

from sqlalchemy import Row, case, func
from sqlalchemy.orm import Query, Session

from app.models.comment import Comment
from app.models.common.status import Status


class CommentDbGateway:
    def __init__(self, session: Session) -> None:
        self.db = session

    def create(self, comment: Comment) -> None:
        self.db.add(comment)
        self.db.commit()

    def get_by_id(self, post_id: int, comment_id: int) -> Comment:
        return (
            self.db.query(Comment)
            .filter(
                Comment.post_id == post_id,
                Comment.id == comment_id,
                Comment.status == Status.ACTIVE,
            )
            .first()
        )

    def get_list_by_post_id(
        self, post_id: int, skip: int, limit: int
    ) -> Tuple[List[Comment], int]:
        query = self.db.query(Comment).filter(
            Comment.post_id == post_id, Comment.status == Status.ACTIVE
        )
        comments = query.offset(skip).limit(limit).all()
        return comments, self.get_total(query)

    def get_list_by_parent_id(
        self, parent_id: int, skip: int, limit: int
    ) -> Tuple[List[Comment], int]:
        query = self.db.query(Comment).filter(
            Comment.parent_comment_id == parent_id, Comment.status == Status.ACTIVE
        )
        comments = query.offset(skip).limit(limit).all()
        return comments, self.get_total(query)

    def update(self, comment: Comment, data: dict) -> None:
        allowed_fields = ["content"]
        for field, value in data.items():
            if field in allowed_fields and value:
                setattr(comment, field, value)
        self.db.commit()

    def delete(self, comment: Comment) -> None:
        self.db.delete(comment)
        self.db.commit()

    def get_total(self, query: Query) -> int:
        return query.count()

    def get_statistics_by_date(
        self, date_from: datetime, date_to: datetime, post_id: int
    ) -> List[Row]:
        return (
            self.db.query(
                func.date(Comment.created_at).label("date"),
                func.count(Comment.id).label("total_comments"),
                func.sum(case((Comment.status == Status.BANNED, 1), else_=0)).label(
                    "banned_comments"
                ),
            )
            .filter(
                Comment.post_id == post_id,
                Comment.created_at >= date_from,
                Comment.created_at <= date_to,
            )
            .group_by(func.date(Comment.created_at))
            .all()
        )
