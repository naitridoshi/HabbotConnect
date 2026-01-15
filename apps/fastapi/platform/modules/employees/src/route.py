from fastapi import APIRouter, Depends, Query
from starlette import status
from starlette.responses import JSONResponse

from apps.fastapi.auth.src import require_user
from apps.fastapi.platform.modules.employees.src.dto import (
    CreateEmployeeDTO,
    EmployeeResponseDTO,
    EmployeesListResponseDTO,
    UpdateEmployeeDTO,
)
from apps.fastapi.platform.modules.employees.src.service import employee_service
from libs.utils.common.custom_logger.src import CustomLogger
from libs.utils.enums.src import DepartmentType, RoleType

log = CustomLogger("EmployeesRoute")
logger, listener = log.get_logger()
listener.start()

employees_route = APIRouter(prefix="/employees", tags=["Employees"])


@employees_route.post(
    "/",
    response_model=EmployeeResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
@log.track
async def create_employee(
    employee_data: CreateEmployeeDTO, current_user=Depends(require_user)
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


@employees_route.get("/", response_model=EmployeesListResponseDTO)
@log.track
async def get_employees(
    current_user=Depends(require_user),
    department: DepartmentType | None = None,
    role: RoleType | None = None,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
):
    try:
        logger.info(f"Employee list request by : {current_user.get('email')}")
        return employee_service.list_employees(department, role, page, page_size)
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


@employees_route.get("/{employee_id}", response_model=EmployeeResponseDTO)
@log.track
async def get_employee(
    employee_id: str,
    current_user=Depends(require_user),
):
    try:
        logger.info(f"Employee fetch request by : {current_user.get('email')}")
        return employee_service.get_employee(employee_id)
    except ValueError as error:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(error)},
        )
    except Exception as error:
        logger.error("Unhandled error during employee fetch request")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Internal Server Error in employee fetch - {str(error)}",
            },
        )


@employees_route.put("/{employee_id}", response_model=EmployeeResponseDTO)
@log.track
async def update_employee(
    employee_id: str,
    updated_data: UpdateEmployeeDTO,
    current_user=Depends(require_user),
):
    try:
        logger.info(f"Employee update request by : {current_user.get('email')}")
        return employee_service.update_employee(
            employee_id, updated_data.model_dump(exclude_unset=True)
        )
    except ValueError as error:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(error)},
        )
    except Exception as error:
        logger.error("Unhandled error during employee update request")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Internal Server Error in employee update - {str(error)}",
            },
        )


@employees_route.delete(
    "/{employee_id}", status_code=status.HTTP_204_NO_CONTENT
)
@log.track
async def delete_employee(
    employee_id: str,
    current_user=Depends(require_user),
):
    try:
        logger.info(f"Employee delete request by : {current_user.get('email')}")
        return employee_service.delete_employee(employee_id)
    except ValueError as error:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(error)},
        )
    except Exception as error:
        logger.error("Unhandled error during employee delete request")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Internal Server Error in employee delete - {str(error)}",
            },
        )
