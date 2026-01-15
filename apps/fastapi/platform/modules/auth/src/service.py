import json
from datetime import datetime, timedelta, timezone

from jose import jwt
from libs.fastapi.platform.modules.auth.src import (
    format_current_user_details,
)
from libs.utils.db.postgres.models.src import User
from libs.utils.db.postgres.operations.src import db_operations

from apps.fastapi.platform.modules.auth.src.dto import (
    AccessTokenData,
    UserLogin,
)
from libs.utils.common.custom_logger.src import CustomLogger
from libs.utils.config.src.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)

log = CustomLogger("AuthService")
logger, listener = log.get_logger()
listener.start()


@log.track
def create_access_token(data: AccessTokenData) -> str:
    to_encode = json.loads(data.model_dump_json())
    logger.debug(
        "Preparing access token payload for user_id=%s role=%s",
        to_encode.get("user_id"),
        getattr(to_encode.get("role"), "value", to_encode.get("role")),
    )
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(
        "Access token generated for user_id=%s exp=%s",
        to_encode.get("user_id"),
        expire.isoformat(),
    )
    return encoded_jwt


@log.track
async def authenticate_user(login_data: UserLogin):
    logger.info("Authenticating user with email=%s", login_data.email)
    user = await db_operations.authenticate(login_data.email, login_data.password)
    if user:
        logger.info("User authentication successful for user_id=%s", user.id)
    else:
        logger.warning("User authentication failed for email=%s", login_data.email)

    return user


@log.track
def get_current_user_details(current_user: User):
    logger.debug("Formatting current user details for user_id=%s", current_user.id)
    details = format_current_user_details(current_user)
    logger.info("Formatted current user details for user_id=%s", current_user.id)
    return details
