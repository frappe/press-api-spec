from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = [
    "Upstream",
    "SetRouteRequest",
    "SetRouteResponse",
    "DeleteRouteResponse",
]


class Upstream(BaseModel):
    address: str = Field(description="Host:port backend address, e.g. 10.2.0.5:8080")
    weight: int = Field(description="Positive integer weight", ge=1)


class SetRouteRequest(BaseModel):
    upstream: str | None = Field(default=None, description="Single upstream target host:port")
    upstreams: list[Upstream] | None = Field(default=None, description="List of upstreams for SWRR")


class SetRouteResponse(BaseModel):
    status: str = Field(default="success", description="Status code")


class DeleteRouteResponse(BaseModel):
    status: str = Field(default="success", description="Status code")
    deleted: bool = Field(description="True if route was deleted, False if not present")
