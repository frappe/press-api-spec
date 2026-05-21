from __future__ import annotations

from typing import TypeAlias

from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.compute_service_v1.models.activity import (
    ListActivityLogsQuery,
    ListActivityLogsResponse,
)
from press_api_spec.compute_service_v1.models.network import (
    CreateNetworkRequest,
    CreateNetworkResponse,
    DeleteNetworkResponse,
    GetNetworkResponse,
    ListNetworksQuery,
    ListNetworksResponse,
    UpdateNetworkRequest,
    UpdateNetworkResponse,
)

__all__ = [
    "NetworkGroup",
    "CreateNetwork",
    "ListNetworks",
    "GetNetwork",
    "UpdateNetwork",
    "DeleteNetwork",
    "ListNetworkActivity",
]


NetworkGroup = EndpointGroup(prefix="/api/networks", tags=("Networks",))


class CreateNetwork(Endpoint):
    method = Method.POST
    path = ""
    name = "create_network"
    summary = "Create a new network"
    Body: TypeAlias = CreateNetworkRequest
    Response: TypeAlias = CreateNetworkResponse


NetworkGroup.add(CreateNetwork)


class ListNetworks(Endpoint):
    method = Method.GET
    path = ""
    name = "list_networks"
    summary = "Return a paginated list of networks"
    Response: TypeAlias = ListNetworksResponse
    Query: TypeAlias = ListNetworksQuery


NetworkGroup.add(ListNetworks)


class GetNetwork(Endpoint):
    method = Method.GET
    path = "/<network_id>"
    name = "get_network"
    summary = "Fetch a single network by id"
    Response: TypeAlias = GetNetworkResponse


NetworkGroup.add(GetNetwork)


class UpdateNetwork(Endpoint):
    method = Method.PATCH
    path = "/<network_id>"
    name = "update_network"
    summary = "Update mutable network attributes (name, description)"
    Body: TypeAlias = UpdateNetworkRequest
    Response: TypeAlias = UpdateNetworkResponse


NetworkGroup.add(UpdateNetwork)


class DeleteNetwork(Endpoint):
    method = Method.DELETE
    path = "/<network_id>"
    name = "delete_network"
    summary = "Delete a network"
    Response: TypeAlias = DeleteNetworkResponse


NetworkGroup.add(DeleteNetwork)


class ListNetworkActivity(Endpoint):
    method = Method.GET
    path = "/<network_id>/activity"
    name = "list_network_activity"
    summary = "List activity log entries for a network"
    Response: TypeAlias = ListActivityLogsResponse
    Query: TypeAlias = ListActivityLogsQuery


NetworkGroup.add(ListNetworkActivity)
