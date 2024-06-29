from sqlalchemy.orm import Session

from app.models.user import User


class UserDbGateway:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, user: User) -> None:
        self.db.add(user)
        self.db.commit()

    def get_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_list(self, skip: int, limit: int) -> list[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_total(self) -> int:
        return self.db.query(User).count()
