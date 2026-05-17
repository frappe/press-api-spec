from __future__ import annotations

from typing import TypeAlias

from press_api_spec.base import Endpoint, EndpointGroup, Method
from press_api_spec.node_agent_service_v1.models.health import HealthResponse

__all__ = ["HealthGroup", "GetHealth"]


HealthGroup = EndpointGroup(prefix="/_meta", tags=("Health",))


class GetHealth(Endpoint):
    method = Method.GET
    path = "/health"
    name = "get_health"
    summary = "Service health probe"
    Response: TypeAlias = HealthResponse


HealthGroup.add(GetHealth)
