from __future__ import annotations

from press_api_spec.base import Endpoint, EndpointGroup
from press_api_spec.node_agent_contract_v1.endpoints.routes import *  # noqa: F401,F403
from press_api_spec.node_agent_contract_v1.endpoints.routes import MetaGroup

ALL_GROUPS: list[EndpointGroup] = [MetaGroup]
ALL_ENDPOINTS: list[type[Endpoint]] = [ep for group in ALL_GROUPS for ep in group]
