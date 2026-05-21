from __future__ import annotations

from typing import TypeAlias

from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.compute_service_v1.models.agent_sync import (
    GetAgentNodeSpecResponse,
    GetVolumeAgentNodeSpecResponse,
    ReportAgentNodeStatusRequest,
    ReportAgentNodeStatusResponse,
    ReportVolumeAgentStatusRequest,
    ReportVolumeAgentStatusResponse,
)

__all__ = [
    "AgentSyncGroup",
    "GetAgentSpec",
    "ReportAgentStatus",
    "VolumeAgentSyncGroup",
    "GetVolumeAgentSpec",
    "ReportVolumeAgentStatus",
]


AgentSyncGroup = EndpointGroup(prefix="/api/runtime-agent", tags=("Agent Sync",))


class GetAgentSpec(Endpoint):
    method = Method.GET
    path = "/spec"
    name = "get_agent_spec"
    summary = "Pull the desired state for this node (networks, stacks); node identity is resolved from the agent auth token"
    Response: TypeAlias = GetAgentNodeSpecResponse


AgentSyncGroup.add(GetAgentSpec)


class ReportAgentStatus(Endpoint):
    method = Method.POST
    path = "/report"
    name = "report_agent_status"
    summary = "Push observed state of networks, stacks, and containers; node identity is resolved from the agent auth token"
    Body: TypeAlias = ReportAgentNodeStatusRequest
    Response: TypeAlias = ReportAgentNodeStatusResponse


AgentSyncGroup.add(ReportAgentStatus)


# ---------------------------------------------------------------------------
# Volume Agent — separated from runtime agent
# ---------------------------------------------------------------------------

VolumeAgentSyncGroup = EndpointGroup(prefix="/api/volume-agent", tags=("Volume Agent Sync",))


class GetVolumeAgentSpec(Endpoint):
    method = Method.GET
    path = "/spec"
    name = "get_volume_agent_spec"
    summary = "Pull the desired state for volumes on this node; node identity is resolved from the agent auth token"
    Response: TypeAlias = GetVolumeAgentNodeSpecResponse


VolumeAgentSyncGroup.add(GetVolumeAgentSpec)


class ReportVolumeAgentStatus(Endpoint):
    method = Method.POST
    path = "/report"
    name = "report_volume_agent_status"
    summary = "Push observed state of volumes on this node; node identity is resolved from the agent auth token"
    Body: TypeAlias = ReportVolumeAgentStatusRequest
    Response: TypeAlias = ReportVolumeAgentStatusResponse


VolumeAgentSyncGroup.add(ReportVolumeAgentStatus)
