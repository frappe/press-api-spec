from __future__ import annotations

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
    "routes",
    "CreateRoute",
    "ListRoutes",
    "GetRoute",
    "UpdateRoute",
    "DeleteRoute",
]

routes = EndpointGroup(prefix="/proxy/domains/<domain_id>/routes", tags=("Routes",))

CreateRoute = routes.add(
    Endpoint(
        method=Method.POST,
        path="",
        body=CreateRouteRequest,
        response=CreateRouteResponse,
        name="create_route",
        summary="Create a route binding a domain to a container",
    )
)

ListRoutes = routes.add(
    Endpoint(
        method=Method.GET,
        path="",
        query=ListRoutesQuery,
        response=ListRoutesResponse,
        name="list_routes",
        summary="List routes for a domain",
    )
)

GetRoute = routes.add(
    Endpoint(
        method=Method.GET,
        path="/<route_id>",
        response=GetRouteResponse,
        name="get_route",
        summary="Get route details",
    )
)

UpdateRoute = routes.add(
    Endpoint(
        method=Method.PATCH,
        path="/<route_id>",
        body=UpdateRouteRequest,
        response=UpdateRouteResponse,
        name="update_route",
        summary="Update mutable route attributes (target_port)",
    )
)

DeleteRoute = routes.add(
    Endpoint(
        method=Method.DELETE,
        path="/<route_id>",
        response=DeleteRouteResponse,
        name="delete_route",
        summary="Delete a route",
    )
)
