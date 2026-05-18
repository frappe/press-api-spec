from __future__ import annotations

from press_api_spec.base import Endpoint, EndpointGroup
from press_api_spec.node_agent_service_v1.endpoints.admin import *  # noqa: F401,F403
from press_api_spec.node_agent_service_v1.endpoints.admin import AdminGroup
from press_api_spec.node_agent_service_v1.endpoints.health import *  # noqa: F401,F403
from press_api_spec.node_agent_service_v1.endpoints.health import HealthGroup
from press_api_spec.node_agent_service_v1.endpoints.node import *  # noqa: F401,F403
from press_api_spec.node_agent_service_v1.endpoints.node import NodeGroup

ALL_GROUPS: list[EndpointGroup] = [HealthGroup, NodeGroup, AdminGroup]
ALL_ENDPOINTS: list[type[Endpoint]] = [ep for group in ALL_GROUPS for ep in group]
