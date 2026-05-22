from __future__ import annotations

from typing import TypeAlias

from press_api_spec.base import Endpoint, EndpointGroup, Method
from press_api_spec.runtime_agent_v1.models.containers import RestartContainerResponse

__all__ = ["RuntimeGroup", "RestartContainer"]

RuntimeGroup = EndpointGroup(prefix="/press-compute-runtime", tags=("Runtime",))


class RestartContainer(Endpoint):
    method = Method.POST
    path = "/containers/<container_id>/restart"
    name = "restart_container"
    summary = "Restart a managed container"
    Response: TypeAlias = RestartContainerResponse
    Body: TypeAlias = None
    Query: TypeAlias = None


RuntimeGroup.add(RestartContainer)
