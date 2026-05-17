from __future__ import annotations

from typing import TypeAlias

from press_api_spec.base import Endpoint, EndpointGroup, Method
from press_api_spec.node_agent_service_v1.models.admin import (
    CheckRequest,
    HasPermissionResponse,
    RefreshAgentQuery,
    RefreshAgentResponse,
)

__all__ = [
    "AdminGroup",
    "RefreshAgent",
    "HasPermission",
]


AdminGroup = EndpointGroup(prefix="/_admin", tags=("Admin",))


class RefreshAgent(Endpoint):
    method = Method.POST
    path = "/refresh-agent"
    name = "refresh_agent"
    summary = "Trigger a route prefix and whitelist refresh for one agent or all agents"
    Query: TypeAlias = RefreshAgentQuery
    Response: TypeAlias = RefreshAgentResponse


AdminGroup.add(RefreshAgent)


class HasPermission(Endpoint):
    method = Method.POST
    path = "/has-permission"
    name = "has_permission"
    summary = "Check whether a subject is authorised to perform an action on a resource"
    Body: TypeAlias = CheckRequest
    Response: TypeAlias = HasPermissionResponse


AdminGroup.add(HasPermission)
