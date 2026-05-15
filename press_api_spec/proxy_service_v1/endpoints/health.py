from __future__ import annotations

from typing import TypeAlias

from press_api_spec.proxy_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.proxy_service_v1.models.health import HealthResponse

__all__ = ["HealthGroup", "GetHealth"]


HealthGroup = EndpointGroup(prefix="", tags=("Health",))

class GetHealth(Endpoint):
    method = Method.GET
    path = "/health"
    name = "get_health"
    summary = "Service health and version probe"
    Response: TypeAlias = HealthResponse

HealthGroup.add(GetHealth)
