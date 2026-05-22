from __future__ import annotations

from typing import TypeAlias

from press_api_spec.tier1_proxy_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.tier1_proxy_service_v1.models.route import (
    Tier1CreateRouteRequest,
    Tier1CreateRouteResponse,
    Tier1DeleteRouteResponse,
)

__all__ = [
    "Tier1RouteGroup",
    "Tier1CreateRoute",
    "Tier1DeleteRoute",
]

Tier1RouteGroup = EndpointGroup(prefix="/proxy/routes", tags=("Routes",))


class Tier1CreateRoute(Endpoint):
    method = Method.PUT
    path = "/<domain>"
    name = "set_route"
    summary = "Set route in Tier 1 proxy"
    Body: TypeAlias = Tier1CreateRouteRequest
    Response: TypeAlias = Tier1CreateRouteResponse


Tier1RouteGroup.add(Tier1CreateRoute)


class Tier1DeleteRoute(Endpoint):
    method = Method.DELETE
    path = "/<domain>"
    name = "delete_route"
    summary = "Delete route from Tier 1 proxy"
    Response: TypeAlias = Tier1DeleteRouteResponse


Tier1RouteGroup.add(Tier1DeleteRoute)
