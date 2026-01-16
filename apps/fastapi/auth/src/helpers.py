import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from libs.utils.common.custom_logger.src import CustomLogger
from libs.utils.config.src.auth import (
    ALGORITHM,
    SECRET_KEY,
)
from libs.utils.db.mongodb.operations.src import users_operations

auth_scheme = HTTPBearer()


log = CustomLogger("AuthHelpers", is_request=False)
logger, listener = log.get_logger()
listener.start()


def require_user(credentials: HTTPAuthorizationCredentials = Security(auth_scheme)):
    token = credentials.credentials
    try:
        user_id = decode_jwt_token(token)
        if not user_id:
            logger.warning("Token missing user_id")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing token subject",
            )
        logger.info(f"Token decoded successfully for user_id: {user_id}")

    except ExpiredSignatureError:
        logger.warning("Expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )

    except InvalidTokenError:
        logger.error("Invalid token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = users_operations.get_user_by_id(user_id)

    if not user:
        logger.warning(f"User not found for user_id: {user_id}")
        raise HTTPException(status_code=401, detail="User not found")

    if not user.get("is_active"):
        logger.warning(f"Inactive account for user_id: {user_id}")
        raise HTTPException(status_code=403, detail="Inactive account")

    logger.info(f"User authenticated successfully: {user_id}")
    return user


def decode_jwt_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    return user_id
