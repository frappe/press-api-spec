from __future__ import annotations

from pydantic import BaseModel, Field

from press_api_spec.tier1_proxy_service_v1.base import EmptyResponse

__all__ = [
    "Tier1Route",
    "Tier1CreateRouteRequest",
    "Tier1CreateRouteResponse",
    "Tier1DeleteRouteResponse",
]


class Tier1Route(BaseModel):
    domain: str = Field(description="Domain name registered in cluster routes")
    target: str = Field(description="Target Tier 2 proxy host:port address, e.g. t2-proxy:443")


class Tier1CreateRouteRequest(BaseModel):
    upstream: str = Field(description="Target Tier 2 proxy host:port address, e.g. t2-proxy:443")


class Tier1CreateRouteResponse(BaseModel):
    ok: bool = True


Tier1DeleteRouteResponse = EmptyResponse
