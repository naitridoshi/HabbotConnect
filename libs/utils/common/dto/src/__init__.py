from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

# Type variable for generic response data
T = TypeVar("T")


class ErrorDetailDTO(BaseModel):
    """Error detail structure."""

    code: str
    message: str
    details: Optional[Any] = None

    class Config:
        populate_by_name = True


class BaseResponseDTO(BaseModel, Generic[T]):
    """Base response structure for all API responses."""

    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    error: Optional[ErrorDetailDTO] = None

    class Config:
        populate_by_name = True


class BaseListResponseDataDTO(BaseModel, Generic[T]):
    """Base structure for paginated list responses."""

    items: List[T]
    total: int
    page: int
    page_size: int = Field(..., alias="pageSize")
    total_pages: int = Field(..., alias="totalPages")

    class Config:
        populate_by_name = True


class BaseListResponseDataWithoutPaginationDTO(BaseModel, Generic[T]):
    """Base structure for list responses without pagination"""

    items: List[T]

    class Config:
        populate_by_name = True


class IdResponseDTO(BaseModel):
    """Response containing only an ID."""

    id: str

    class Config:
        populate_by_name = True
