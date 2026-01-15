from fastapi import APIRouter
from fastapi.security import (
    HTTPBearer,
)
from starlette.responses import JSONResponse

from apps.fastapi.platform.modules.auth.src.dto import (
    LoginResponseDTO,
    UserLoginDTO,
    UserRegisterDTO,
)
from apps.fastapi.platform.modules.auth.src.service import (
    login_user,
    signup_user,
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
    try:
        logger.info(f"Login attempt started for email {login_data.email}")
        return login_user(login_data)

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


@auth_route.post("/signup", response_model=LoginResponseDTO)
@log.track
async def signup(
    signup_data: UserRegisterDTO,
):
    try:
        logger.info(f"Signup attempt started for email {signup_data.email}")
        return signup_user(signup_data)

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
