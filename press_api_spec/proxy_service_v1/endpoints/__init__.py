from __future__ import annotations

from typing import Any

from press_api_spec.proxy_service_v1.base import Endpoint, EndpointGroup
from press_api_spec.proxy_service_v1.endpoints.action import *  # noqa: F401,F403
from press_api_spec.proxy_service_v1.endpoints.action import ActionGroup
from press_api_spec.proxy_service_v1.endpoints.domain import *  # noqa: F401,F403
from press_api_spec.proxy_service_v1.endpoints.domain import DomainGroup
from press_api_spec.proxy_service_v1.endpoints.health import *  # noqa: F401,F403
from press_api_spec.proxy_service_v1.endpoints.health import HealthGroup
from press_api_spec.proxy_service_v1.endpoints.redirect import *  # noqa: F401,F403
from press_api_spec.proxy_service_v1.endpoints.redirect import RedirectGroup
from press_api_spec.proxy_service_v1.endpoints.route import *  # noqa: F401,F403
from press_api_spec.proxy_service_v1.endpoints.route import RouteGroup

ALL_GROUPS: list[EndpointGroup] = [DomainGroup, RedirectGroup, RouteGroup, HealthGroup, ActionGroup]
ALL_ENDPOINTS: list[Endpoint[Any, Any]] = [ep for group in ALL_GROUPS for ep in group]
