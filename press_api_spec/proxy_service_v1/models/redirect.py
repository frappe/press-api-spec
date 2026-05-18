from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

from press_api_spec.proxy_service_v1.base import EmptyResponse, Paginated, PaginationParams

__all__ = [
    "MatchType",
    "RedirectStatus",
    "RedirectRule",
    "CreateRedirectRequest",
    "UpdateRedirectRequest",
    "CreateRedirectResponse",
    "UpdateRedirectResponse",
    "ListRedirectsQuery",
    "ListRedirectsResponse",
    "GetRedirectResponse",
    "DeleteRedirectResponse",
]


class MatchType(str, Enum):
    EXACT = "exact"
    PREFIX = "prefix"
    REGEX = "regex"


class RedirectStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    ERROR = "error"


class RedirectRule(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "redir_xyz789",
                    "domain_id": "dom_abc123",
                    "source_path": "/blog/*",
                    "match_type": "prefix",
                    "target_url": "https://blog.example.com/",
                    "status_code": 301,
                    "status": "active",
                    "created_at_unix": 1736935200,
                    "updated_at_unix": 1736942400,
                }
            ]
        }
    )

    id: str
    domain_id: str
    source_path: str = Field(examples=["/old-path", "/blog/*", "^/v1/.*"])
    match_type: MatchType
    target_url: str = Field(examples=["https://example.com/new-path", "https://blog.example.com/"])
    status_code: int = Field(examples=[301, 302, 307, 308])
    status: RedirectStatus = RedirectStatus.PENDING
    created_at_unix: int
    updated_at_unix: int


class CreateRedirectRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "source_path": "/blog/*",
                    "match_type": "prefix",
                    "target_url": "https://blog.example.com/",
                    "status_code": 301,
                }
            ]
        }
    )

    source_path: str = Field(examples=["/old-path", "/blog/*", "^/v1/.*"])
    match_type: MatchType
    target_url: str = Field(examples=["https://example.com/new-path", "https://blog.example.com/"])
    status_code: int = Field(examples=[301, 302, 307, 308])


class UpdateRedirectRequest(BaseModel):
    source_path: str | None = Field(default=None, examples=["/new-path", "/docs/*"])
    match_type: MatchType | None = None
    target_url: str | None = Field(default=None, examples=["https://example.com/updated"])
    status_code: int | None = Field(default=None, examples=[301, 302])


class CreateRedirectResponse(BaseModel):
    redirect: RedirectRule


class UpdateRedirectResponse(BaseModel):
    redirect: RedirectRule


class ListRedirectsQuery(PaginationParams):
    status: RedirectStatus | None = None
    match_type: MatchType | None = None


ListRedirectsResponse = Paginated[RedirectRule]


class GetRedirectResponse(BaseModel):
    redirect: RedirectRule


DeleteRedirectResponse = EmptyResponse
