from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from libs.utils.common.dto.src import BaseResponseDTO
from libs.utils.enums.src import TokenType


class UserLoginDTO(BaseModel):
    email: EmailStr = Field("user@gmail.com")
    password: str = Field("user123")


class UserRegisterDTO(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)


class LoginDataDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: TokenType
    email: EmailStr


class LoginResponseDTO(BaseResponseDTO[LoginDataDTO]):
    pass


class RegisterDataDTO(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)


class RegisterResponseDTO(BaseResponseDTO[RegisterDataDTO]):
    pass
