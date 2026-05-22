from __future__ import annotations

from typing import TypeAlias

from press_api_spec.tier2_proxy_service_v2.base import Endpoint, EndpointGroup, Method
from press_api_spec.tier2_proxy_service_v2.models.route import (
    DeleteRouteResponse,
    SetRouteRequest,
    SetRouteResponse,
)

__all__ = ["RouteGroup", "SetRoute", "DeleteRoute"]

RouteGroup = EndpointGroup(prefix="/proxy/routes", tags=("Routes",))


class SetRoute(Endpoint):
    method = Method.PUT
    path = "/<domain>"
    name = "set_route"
    summary = "Set single or weighted upstreams route for a domain"
    Body: TypeAlias = SetRouteRequest
    Response: TypeAlias = SetRouteResponse


RouteGroup.add(SetRoute)


class DeleteRoute(Endpoint):
    method = Method.DELETE
    path = "/<domain>"
    name = "delete_route"
    summary = "Delete upstream route for a domain"
    Response: TypeAlias = DeleteRouteResponse


RouteGroup.add(DeleteRoute)
