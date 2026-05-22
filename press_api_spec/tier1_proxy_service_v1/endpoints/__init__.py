from __future__ import annotations

from press_api_spec.tier1_proxy_service_v1.base import Endpoint, EndpointGroup
from press_api_spec.tier1_proxy_service_v1.endpoints.route import *  # noqa: F401,F403
from press_api_spec.tier1_proxy_service_v1.endpoints.route import Tier1RouteGroup

ALL_GROUPS: list[EndpointGroup] = [Tier1RouteGroup]
ALL_ENDPOINTS: list[type[Endpoint]] = [ep for group in ALL_GROUPS for ep in group]

__all__ = ["ALL_ENDPOINTS", "ALL_GROUPS"]
