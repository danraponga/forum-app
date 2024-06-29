from app.core.exceptions import AccessDenied


class BaseService:
    def ensure_can_edit(self, owner_id: int, user_id: int) -> None:
        if not owner_id == user_id:
            raise AccessDenied()
