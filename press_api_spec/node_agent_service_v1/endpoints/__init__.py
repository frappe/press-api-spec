from __future__ import annotations

from typing import Any

from press_api_spec.base import Endpoint, EndpointGroup
from press_api_spec.node_agent_service_v1.endpoints.admin import *  # noqa: F401,F403
from press_api_spec.node_agent_service_v1.endpoints.admin import AdminGroup
from press_api_spec.node_agent_service_v1.endpoints.health import *  # noqa: F401,F403
from press_api_spec.node_agent_service_v1.endpoints.health import HealthGroup

ALL_GROUPS: list[EndpointGroup] = [HealthGroup, AdminGroup]
ALL_ENDPOINTS: list[Endpoint[Any, Any]] = [ep for group in ALL_GROUPS for ep in group]
