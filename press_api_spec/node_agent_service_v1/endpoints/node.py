from __future__ import annotations

from typing import TypeAlias

from press_api_spec.base import Endpoint, EndpointGroup, Method
from press_api_spec.node_agent_service_v1.models.node import (
    GetNodeInfoResponse,
    UpdateNodeStatusRequest,
    UpdateNodeStatusResponse,
)

__all__ = [
    "NodeGroup",
    "GetNodeInfo",
    "UpdateNodeStatus",
]


NodeGroup = EndpointGroup(prefix="/api/node", tags=("Node",))


class GetNodeInfo(Endpoint):
    method = Method.GET
    path = ""
    name = "get_node_info"
    summary = "Get node information and resource capacity"
    Response: TypeAlias = GetNodeInfoResponse


NodeGroup.add(GetNodeInfo)


class UpdateNodeStatus(Endpoint):
    method = Method.PATCH
    path = "/status"
    name = "update_node_status"
    summary = "Update node status (e.g. ready, draining, offline)"
    Body: TypeAlias = UpdateNodeStatusRequest
    Response: TypeAlias = UpdateNodeStatusResponse


NodeGroup.add(UpdateNodeStatus)
