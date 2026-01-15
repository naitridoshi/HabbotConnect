from libs.fastapi.platform.modules.auth.src import (
    get_password_hash,
    verify_password,
)
from libs.utils.common.custom_logger.src import CustomLogger
from libs.utils.db.mongodb.operations.src.base import BaseOperations
from libs.utils.db.mongodb.src.repository import users_repository

log = CustomLogger("UsersOperations", is_request=False)
logger, listener = log.get_logger()
listener.start()


class UsersOperations(BaseOperations):
    def __init__(self):
        super().__init__(users_repository)

    def get_user_by_email(self, email: str):
        return self._repository.find_one({"email": email, "is_active": True})

    def authenticate(self, email: str, password: str):
        try:
            user = self.get_user_by_email(email)
            if not user:
                return None
            if not verify_password(password, user.get("password")):
                return None
            return user
        except Exception as e:
            logger.error(f"Error in authenticate: {e}", exc_info=True)
            raise

    def get_user_by_id(self, user_id: str):
        return self.find_by_id(user_id)

    def create_user(self, name: str, email: str, password: str):
        try:
            hashed_password = get_password_hash(password)
            user = self._repository.insert_one(
                {
                    "email": email,
                    "password": hashed_password,
                    "name": name,
                }
            )
            return user
        except Exception as e:
            logger.error(f"Error in create_user: {e}", exc_info=True)
            raise
