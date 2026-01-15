from datetime import date, datetime
from typing import Optional
from uuid import UUID

from libs.fastapi.platform.modules.users.src import validate_password
from libs.utils.enums.src.auth import SupportedRoles
from libs.utils.enums.src.case import CaseApprovalStatus, CaseStatus
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)


class ResponseMessage(BaseModel):
    success: bool
    message: str


class UserLogin(BaseModel):
    email: EmailStr = Field("user@gmail.com")
    password: str = Field("user123")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AccessTokenData(BaseModel):
    user_id: UUID | None = None
    role: SupportedRoles | None = None
    email: EmailStr
    is_email_verified: bool | None = None

    model_config = {
        "json_encoders": {SupportedRoles: lambda v: v.value, UUID: lambda v: str(v)}
    }


class LoginResponse(ResponseMessage):
    access_token: str
    token_type: str
    role: SupportedRoles
    email: EmailStr
    is_email_verified: bool | None = None

    class Config:
        from_attributes = True


class ResendVerificationRequest(BaseModel):
    email: EmailStr


class CaseDetails(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: UUID
    name: str
    case_id: str
    amount_to_pay: float
    amount_present: float
    frequency: int
    status: CaseStatus
    approval_status: CaseApprovalStatus
    payer_id: UUID
    recipient_id: UUID
    payer_wallet_id: UUID | None = None
    recipient_wallet_id: UUID | None = None
    rule_id: UUID | None = None
    due_day: int
    active_until: date
    child_name: str
    child_date_of_birth: date
    funds_blocked: bool
    created_at: datetime
    updated_at: datetime


class CaseResponse(ResponseMessage):
    case_details: CaseDetails


class InviteUserRequest(BaseModel):
    recipient_email: EmailStr
    message: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional note that will be shared with the invitee.",
    )


class ResetPasswordViaTokenRequest(BaseModel):
    new_password: str = Field(..., min_length=8)
    confirm_new_password: str = Field(..., min_length=8)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.new_password != self.confirm_new_password:
            raise ValueError("New passwords do not match.")
        return self

    @field_validator("new_password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        if v and not validate_password(v):
            raise ValueError(
                "Password must be 8+ chars with upper, lower, digit, and special character."
            )
        return v
