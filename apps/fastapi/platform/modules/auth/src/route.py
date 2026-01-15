from fastapi import APIRouter, Depends
from fastapi.security import (
    HTTPBearer,
)
from starlette.responses import JSONResponse

from apps.fastapi.auth.src import require_user
from apps.fastapi.platform.modules.auth.src.dto import (
    AccessTokenData,
    LoginResponse,
    UserLogin,
)
from apps.fastapi.platform.modules.auth.src.service import (
    authenticate_user,
    create_access_token,
    get_current_user_details,
)
from libs.utils.common.custom_logger.src import CustomLogger

log = CustomLogger("AuthRoute")
logger, listener = log.get_logger()
listener.start()

auth_route = APIRouter(prefix="/auth", tags=["Auth"])

security = HTTPBearer()


@auth_route.post("/login", response_model=LoginResponse)
@log.track
async def login_access_token(
    login_data: UserLogin,
):
    try:
        logger.info("Login attempt started for email=%s", login_data.email)
        user_authenticated = await authenticate_user(login_data)
        if not user_authenticated:
            logger.warning("Login failed: Incorrect email or password")
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Incorrect email or password"},
            )

        logger.info(
            f"User authenticated successfully: {user_authenticated.id} - role: {user_authenticated.role.value}"
        )
        token = create_access_token(
            data=AccessTokenData(
                user_id=user_authenticated.id,
                role=user_authenticated.role,
                email=user_authenticated.email,
                is_email_verified=user_authenticated.is_email_verified,
            ),
        )

        logger.info("Access token created for user: %s", user_authenticated.id)
        return {
            "success": True,
            "message": "Login successful",
            "access_token": token,
            "token_type": "bearer",
            "role": user_authenticated.role.value,
            "email": user_authenticated.email,
            "is_email_verified": user_authenticated.is_email_verified,
        }
    except ValueError as error:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(error)},
        )
    except Exception as error:
        logger.error("Unhandled error during login for email=%s", login_data.email)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Internal Server Error in logging in - {str(error)}",
            },
        )


@auth_route.get("/me")
@log.track
async def read_current_user(
    current_user=Depends(require_user()),
):
    try:
        logger.info(
            "Fetching current user details for token subject user_id=%s",
            current_user.id,
        )
        user_details = get_current_user_details(current_user)
        logger.debug(
            "Current user details prepared for user_id=%s keys=%s",
            current_user.id,
            list(user_details.keys()),
        )
        return {
            "success": True,
            "message": "User details fetched successfully!",
            "user_details": user_details,
        }
    except Exception as error:
        logger.error(
            "Internal error while returning current user details for user_id=%s",
            getattr(current_user, "id", None),
        )
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Internal Server Error in fetching user details - {str(error)}",
            },
        )
