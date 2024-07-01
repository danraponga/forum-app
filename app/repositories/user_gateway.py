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

    def get_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def get_list(self, skip: int, limit: int) -> tuple[list[User], int]:
        return (
            self.db.query(User).offset(skip).limit(limit).all(),
            self.get_total(),
        )

    def get_total(self) -> int:
        return self.db.query(User).count()
