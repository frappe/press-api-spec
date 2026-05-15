from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from press_api_spec.base import (
    EmptyResponse,
    Endpoint,
    EndpointGroup,
    ErrorCode,
    ErrorDetail,
    ErrorResponse,
    Method,
    Paginated,
    PaginationInfo,
    PaginationParams,
)

__all__ = [
    "Method",
    "Endpoint",
    "EndpointGroup",
    "PaginationParams",
    "PaginationInfo",
    "Paginated",
    "EmptyResponse",
    "ErrorCode",
    "ErrorDetail",
    "ErrorResponse",
    "ActionStatus",
    "ActionName",
    "ResourceType",
    "ActionRecord",
]


class ActionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ActionName(str, Enum):
    VERIFY_DOMAIN = "verify_domain"
    RENEW_CERTIFICATE = "renew_certificate"


class ResourceType(str, Enum):
    DOMAIN = "domain"
    REDIRECT = "redirect"
    ROUTE = "route"


class ActionRecord(BaseModel):
    id: str
    name: ActionName
    resource_type: ResourceType
    resource_id: str
    description: str | None = None
    status: ActionStatus = ActionStatus.PENDING
    progress: int = Field(default=0, ge=0, le=100, description="Completion percentage (0-100)")
    result: dict[str, Any] | None = None
    error: str | None = Field(default=None, description="Error message if status is failed")
    started_at_unix: int | None = Field(
        default=None, description="UTC timestamp in seconds since epoch"
    )
    finished_at_unix: int | None = Field(
        default=None, description="UTC timestamp in seconds since epoch"
    )
    created_at_unix: int = Field(
        description="UTC timestamp in seconds since epoch", examples=[1736935200]
    )
    updated_at_unix: int = Field(
        description="UTC timestamp in seconds since epoch", examples=[1736942400]
    )
