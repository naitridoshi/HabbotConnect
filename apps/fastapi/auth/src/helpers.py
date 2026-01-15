from typing import List, Optional

import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from libs.utils.db.postgres.models.src import User
from libs.utils.db.postgres.operations.src import db_operations
from libs.utils.enums.src.auth import SupportedRoles

from libs.utils.common.custom_logger.src import CustomLogger
from libs.utils.config.src.auth import (
    ALGORITHM,
    SECRET_KEY,
)

auth_scheme = HTTPBearer()


log = CustomLogger("AuthHelpers", is_request=False)
logger, listener = log.get_logger()
listener.start()


def require_user(
    allowed_roles: Optional[List[SupportedRoles]] = None,
    *,
    enforce_active: bool = True,
    enforce_verified: bool = True,
):
    if allowed_roles is None:
        allowed_roles = list(SupportedRoles)

    async def dep(
        credentials: HTTPAuthorizationCredentials = Security(auth_scheme),
    ) -> User:
        token = credentials.credentials
        logger.info("get_current_user called")
        try:
            user_id = decode_jwt_token(token)
            if not user_id:
                logger.warning("Token missing user_id")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Missing token subject",
                )
            logger.info("Token decoded successfully for user_id: %s", user_id)
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

        user = await db_operations.get_user_by_id(user_id)

        if not user:
            logger.warning("User not found for user_id: %s", user_id)
            raise HTTPException(status_code=401, detail="User not found")

        if enforce_active and not getattr(user, "is_active", False):
            logger.warning("Inactive account for user_id: %s", user_id)
            raise HTTPException(status_code=403, detail="Inactive account")

        if (
            enforce_verified
            and not user.is_email_verified
            and user.role != SupportedRoles.ADMIN
        ):
            logger.warning("Email not verified for user_id: %s", user_id)
            raise HTTPException(status_code=403, detail="Email not verified")

        if allowed_roles and getattr(user, "role", None) not in allowed_roles:
            logger.warning("Insufficient permissions for user_id: %s", user_id)
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        logger.info(
            f"User authenticated successfully: {user_id} - role: {user.role.value}"
        )
        return user

    return dep


def decode_jwt_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    return user_id


def verify_email_verification_token(
    token: str, test_only: bool = False
) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not test_only:
            if payload.get("purpose") != "email_verification":
                return None
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def verify_case_action_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("purpose") != "case_approval":
            return None
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def verify_forget_password_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("purpose") != "forget_password":
            return None
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
