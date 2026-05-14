from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

from press_api_spec.proxy_service_v1.base import EmptyResponse, Paginated, PaginationParams

__all__ = [
    "Protocol",
    "TargetType",
    "RouteStatus",
    "Route",
    "CreateRouteRequest",
    "CreateRouteResponse",
    "ListRoutesQuery",
    "ListRoutesResponse",
    "GetRouteResponse",
    "UpdateRouteRequest",
    "UpdateRouteResponse",
    "DeleteRouteResponse",
]


class Protocol(str, Enum):
    HTTPS = "https"


class TargetType(str, Enum):
    STACK = "stack"


class RouteStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    ERROR = "error"


class Route(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "route_xyz789",
                    "domain_id": "dom_abc123",
                    "target_type": "stack",
                    "target_id": "stack_abc123",
                    "protocol": "https",
                    "port": 443,
                    "target_port": 8080,
                    "status": "active",
                    "created_at_unix": 1736935200,
                    "updated_at_unix": 1736942400,
                }
            ]
        }
    )

    id: str
    domain_id: str
    target_type: TargetType
    target_id: str
    protocol: Protocol
    port: int = Field(examples=[80, 443])
    target_port: int = Field(examples=[8080, 3000])
    status: RouteStatus = RouteStatus.PENDING
    created_at_unix: int
    updated_at_unix: int


class CreateRouteRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "target_type": "stack",
                    "target_id": "stack_abc123",
                    "protocol": "https",
                    "port": 443,
                    "target_port": 8080,
                }
            ]
        }
    )

    target_type: TargetType
    target_id: str
    protocol: Protocol
    port: int = Field(examples=[80, 443])
    target_port: int = Field(examples=[8080, 3000])


class CreateRouteResponse(BaseModel):
    route: Route


class ListRoutesQuery(PaginationParams):
    status: RouteStatus | None = None
    target_id: str | None = Field(default=None, examples=["stack_abc123"])


ListRoutesResponse = Paginated[Route]


class GetRouteResponse(BaseModel):
    route: Route


class UpdateRouteRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={"examples": [{"target_port": 9090}]})

    target_port: int = Field(examples=[8080, 9090, 3000])


class UpdateRouteResponse(BaseModel):
    route: Route


DeleteRouteResponse = EmptyResponse
