from __future__ import annotations

from press_api_spec.runtime_agent_service_v1.base import Endpoint, EndpointGroup
from press_api_spec.runtime_agent_service_v1.endpoints.action import *  # noqa: F401,F403
from press_api_spec.runtime_agent_service_v1.endpoints.action import RuntimeAgentActionGroup

ALL_GROUPS: list[EndpointGroup] = [RuntimeAgentActionGroup]
ALL_ENDPOINTS: list[type[Endpoint]] = [ep for group in ALL_GROUPS for ep in group]

__all__ = ["ALL_ENDPOINTS", "ALL_GROUPS"]
