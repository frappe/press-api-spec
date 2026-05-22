from __future__ import annotations

from typing import TypeAlias

from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.compute_service_v1.models.action import RuntimeAgentActionResponse

__all__ = [
    "RuntimeAgentActionGroup",
    "RestartRuntimeStack",
    "RestartRuntimeContainer",
]


RuntimeAgentActionGroup = EndpointGroup(
    prefix="/press-compute-runtime",
    tags=("Runtime Agent Actions",),
)


class RestartRuntimeStack(Endpoint):
    method = Method.POST
    path = "/stacks/<stack_id>/actions/restart"
    name = "restart_runtime_stack"
    summary = "Restart a stack on the runtime agent without changing desired state"
    Response: TypeAlias = RuntimeAgentActionResponse


RuntimeAgentActionGroup.add(RestartRuntimeStack)


class RestartRuntimeContainer(Endpoint):
    method = Method.POST
    path = "/stacks/<stack_id>/containers/<container_id>/actions/restart"
    name = "restart_runtime_container"
    summary = "Restart a container on the runtime agent without changing desired state"
    Response: TypeAlias = RuntimeAgentActionResponse


RuntimeAgentActionGroup.add(RestartRuntimeContainer)
