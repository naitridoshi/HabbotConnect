from enum import Enum


class TokenType(Enum):
    Bearer = "Bearer"


class DepartmentType(str, Enum):
    HR = "HR"
    SALES = "SALES"
    ENGINEERING = "ENGINEERING"


class RoleType(str, Enum):
    MANAGER = "MANAGER"
    DEVELOPER = "DEVELOPER"
    ANALYST = "ANALYST"
