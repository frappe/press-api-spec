from __future__ import annotations

from press_api_spec.proxy_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.proxy_service_v1.models.health import HealthResponse

__all__ = ["health", "GetHealth"]


health = EndpointGroup(prefix="", tags=("Health",))

GetHealth = health.add(
    Endpoint(
        method=Method.GET,
        path="/health",
        response=HealthResponse,
        name="get_health",
        summary="Service health and version probe",
    )
)
