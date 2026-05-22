from __future__ import annotations

from press_api_spec.base import Endpoint, EndpointGroup
from press_api_spec.runtime_agent_v1.endpoints.containers import *  # noqa: F401,F403
from press_api_spec.runtime_agent_v1.endpoints.containers import RuntimeGroup

ALL_GROUPS: list[EndpointGroup] = [RuntimeGroup]
ALL_ENDPOINTS: list[type[Endpoint]] = [ep for group in ALL_GROUPS for ep in group]
