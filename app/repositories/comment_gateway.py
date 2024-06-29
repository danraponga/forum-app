from sqlalchemy.orm import Query, Session

from app.models.comment import Comment


class CommentDbGateway:
    def __init__(self, session: Session):
        self.db = session

    def create(self, comment: Comment) -> None:
        self.db.add(comment)
        self.db.commit()

    def get_by_id(self, post_id: int, comment_id: int) -> Comment:
        return (
            self.db.query(Comment)
            .filter(Comment.post_id == post_id, Comment.id == comment_id)
            .first()
        )

    def get_list_by_post_id(
        self, post_id: int, skip: int, limit: int
    ) -> tuple[list[Comment], int]:
        query = self.db.query(Comment).filter(Comment.post_id == post_id)
        comments = query.offset(skip).limit(limit).all()
        return comments, self.get_total(query)

    def get_list_by_parent_id(
        self, parent_id: int, skip: int, limit: int
    ) -> tuple[list[Comment], int]:
        query = self.db.query(Comment).filter(Comment.parent_comment_id == parent_id)
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

    def get_total(self, query: Query):
        return query.count()
