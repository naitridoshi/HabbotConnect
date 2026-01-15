from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
)

from libs.utils.common.dto.src import BaseListResponseDataDTO, BaseResponseDTO
from libs.utils.enums.src import DepartmentType, RoleType


class CreateEmployeeDTO(BaseModel):
    name: str
    email: EmailStr
    department: DepartmentType
    role: RoleType


class EmployeeDataDTO(CreateEmployeeDTO):
    id: str
    date_joined: datetime


class EmployeeResponseDTO(BaseResponseDTO[EmployeeDataDTO]):
    pass


class EmployeeListDataDTO(BaseListResponseDataDTO[EmployeeDataDTO]):
    pass


class EmployeesListResponseDTO(BaseResponseDTO[EmployeeListDataDTO]):
    pass
