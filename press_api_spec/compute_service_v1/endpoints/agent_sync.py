from __future__ import annotations

from typing import TypeAlias

from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.compute_service_v1.models.agent_sync import (
    GetAgentNodeSpecResponse,
    ReportAgentNodeStatusRequest,
    ReportAgentNodeStatusResponse,
)

__all__ = [
    "AgentSyncGroup",
    "GetAgentSpec",
    "ReportAgentStatus",
]


AgentSyncGroup = EndpointGroup(prefix="/api/agent", tags=("Agent Sync",))


class GetAgentSpec(Endpoint):
    method = Method.GET
    path = "/spec"
    name = "get_agent_spec"
    summary = "Pull the full desired state for this node (networks, volumes, stacks); node identity is resolved from the agent auth token"
    Response: TypeAlias = GetAgentNodeSpecResponse


AgentSyncGroup.add(GetAgentSpec)


class ReportAgentStatus(Endpoint):
    method = Method.POST
    path = "/report"
    name = "report_agent_status"
    summary = "Push observed state of networks, volumes, stacks, and containers; node identity is resolved from the agent auth token"
    Body: TypeAlias = ReportAgentNodeStatusRequest
    Response: TypeAlias = ReportAgentNodeStatusResponse


AgentSyncGroup.add(ReportAgentStatus)
