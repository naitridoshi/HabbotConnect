from fastapi import APIRouter
from fastapi.security import (
    HTTPBearer,
)
from starlette.responses import JSONResponse

from apps.fastapi.auth.src import require_user
from apps.fastapi.platform.modules.employees.src.dto import (
    CreateEmployeeDTO,
    EmployeeResponseDTO,
    EmployeesListResponseDTO,
)
from apps.fastapi.platform.modules.employees.src.service import employee_service
from libs.utils.common.custom_logger.src import CustomLogger

log = CustomLogger("EmployeesRoute")
logger, listener = log.get_logger()
listener.start()

security = HTTPBearer()

employees_route = APIRouter(prefix="/employees", tags=["Employees"])


@employees_route.post("/employees", response_model=EmployeeResponseDTO)
@log.track
async def create_employee(
    employee_data: CreateEmployeeDTO, current_user=require_user()
):
    try:
        logger.info(f"Employee creation request by : {current_user.get('email')}")
        return employee_service.create_employee(employee_data)

    except ValueError as error:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(error)},
        )
    except Exception as error:
        logger.error(
            f"Unhandled error during employee creation for email {employee_data.email}"
        )
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Internal Server Error in employee creation - {str(error)}",
            },
        )


@employees_route.get("/employees", response_model=EmployeesListResponseDTO)
@log.track
async def get_employees(
    current_user=require_user(),
):
    try:
        logger.info(f"Employee list request by : {current_user.get('email')}")
        return employee_service.list_employees(current_user)
    except ValueError as error:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(error)},
        )
    except Exception as error:
        logger.error("Unhandled error during employee list request")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Internal Server Error in employee list - {str(error)}",
            },
        )
