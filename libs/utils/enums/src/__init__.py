from enum import Enum


class TokenType(Enum):
    Bearer = "Bearer"


class DepartmentType(Enum):
    HR = "HR"
    SALES = "SALES"
    ENGINEERING = "ENGINEERING"


class RoleType(Enum):
    MANAGER = "MANAGER"
    DEVELOPER = "DEVELOPER"
    ANALYST = "ANALYST"
