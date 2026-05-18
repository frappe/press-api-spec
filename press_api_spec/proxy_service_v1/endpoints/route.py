from __future__ import annotations

from typing import TypeAlias

from press_api_spec.proxy_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.proxy_service_v1.models.route import (
    CreateRouteRequest,
    CreateRouteResponse,
    DeleteRouteResponse,
    GetRouteResponse,
    ListRoutesQuery,
    ListRoutesResponse,
    UpdateRouteRequest,
    UpdateRouteResponse,
)

__all__ = [
    "RouteGroup",
    "CreateRoute",
    "ListRoutes",
    "GetRoute",
    "UpdateRoute",
    "DeleteRoute",
]

RouteGroup = EndpointGroup(prefix="/api/proxy/domains/<domain_id>/routes", tags=("Routes",))

class CreateRoute(Endpoint):
    method = Method.POST
    path = ""
    name = "create_route"
    summary = "Create a route binding a domain to a container"
    Body: TypeAlias = CreateRouteRequest
    Response: TypeAlias = CreateRouteResponse

RouteGroup.add(CreateRoute)

class ListRoutes(Endpoint):
    method = Method.GET
    path = ""
    name = "list_routes"
    summary = "List routes for a domain"
    Response: TypeAlias = ListRoutesResponse
    Query: TypeAlias = ListRoutesQuery

RouteGroup.add(ListRoutes)

class GetRoute(Endpoint):
    method = Method.GET
    path = "/<route_id>"
    name = "get_route"
    summary = "Get route details"
    Response: TypeAlias = GetRouteResponse

RouteGroup.add(GetRoute)

class UpdateRoute(Endpoint):
    method = Method.PATCH
    path = "/<route_id>"
    name = "update_route"
    summary = "Update mutable route attributes (target_port)"
    Body: TypeAlias = UpdateRouteRequest
    Response: TypeAlias = UpdateRouteResponse

RouteGroup.add(UpdateRoute)

class DeleteRoute(Endpoint):
    method = Method.DELETE
    path = "/<route_id>"
    name = "delete_route"
    summary = "Delete a route"
    Response: TypeAlias = DeleteRouteResponse

RouteGroup.add(DeleteRoute)
