from fastapi import APIRouter
from fastapi.security import (
    HTTPBearer,
)
from starlette import status
from starlette.responses import JSONResponse

from apps.fastapi.platform.modules.auth.src.dto import (
    LoginResponseDTO,
    RegisterResponseDTO,
    UserLoginDTO,
    UserRegisterDTO,
)
from apps.fastapi.platform.modules.auth.src.service import (
    auth_service,
)
from libs.utils.common.custom_logger.src import CustomLogger

log = CustomLogger("AuthRoute")
logger, listener = log.get_logger()
listener.start()

security = HTTPBearer()

auth_route = APIRouter(prefix="/auth", tags=["Auth"])


@auth_route.post("/login", response_model=LoginResponseDTO)
@log.track
async def login(
    login_data: UserLoginDTO,
):
    """Authenticate a user and return access tokens."""
    try:
        logger.info(f"Login attempt started for email {login_data.email}")
        return auth_service.login_user(login_data)

    except ValueError as error:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(error)},
        )
    except Exception as error:
        logger.error(f"Unhandled error during login for email {login_data.email}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Internal Server Error in logging in - {str(error)}",
            },
        )


@auth_route.post(
    "/signup", response_model=RegisterResponseDTO, status_code=status.HTTP_201_CREATED
)
@log.track
async def signup(
    signup_data: UserRegisterDTO,
):
    """Register a new user account."""
    try:
        logger.info(f"Signup attempt started for email {signup_data.email}")
        return auth_service.signup_user(signup_data)

    except ValueError as error:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(error)},
        )
    except Exception as error:
        logger.error(f"Unhandled error during signup for email {signup_data.email}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Internal Server Error in logging in - {str(error)}",
            },
        )
