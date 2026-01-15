from datetime import timedelta

from apps.fastapi.platform.modules.auth.src.dto import (
    UserLoginDTO,
    UserRegisterDTO,
)
from libs.fastapi.platform.modules.auth.src import create_token
from libs.utils.common.custom_logger.src import CustomLogger
from libs.utils.common.responses.src import success_response
from libs.utils.config.src.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from libs.utils.db.mongodb.operations.src import users_operations
from libs.utils.enums.src import TokenType

log = CustomLogger("AuthService")
logger, listener = log.get_logger()
listener.start()


class AuthService:
    @staticmethod
    @log.track
    def login_user(login_data: UserLoginDTO):
        user_authenticated = users_operations.authenticate(
            login_data.email, login_data.password
        )

        if user_authenticated:
            logger.warning("Login failed: Incorrect email or password")
            raise ValueError("Incorrect email or password")

        access_token = create_token(
            data=login_data.model_dump(),
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        refresh_token = create_token(
            data=login_data.model_dump(),
            expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        )

        return success_response(
            data={
                "id": str(user_authenticated.get("_id")),
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": TokenType.Bearer,
                "role": user_authenticated.get("role"),
                "email": user_authenticated.get("email"),
            },
            message="Successfully logged in",
        )

    @staticmethod
    @log.track
    def signup_user(signup_data: UserRegisterDTO):
        user_with_same_email_exists = users_operations.get_user_by_email(
            signup_data.email
        )
        if user_with_same_email_exists:
            raise ValueError("Email already exists")

        created_id = users_operations.create_user(
            signup_data.email, signup_data.password
        )

        return success_response(
            data={
                "id": str(created_id),
                "name": signup_data.name,
                "email": signup_data.email,
            },
            message="Successfully registered",
        )


auth_service = AuthService()
