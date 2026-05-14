from __future__ import annotations

from typing import Any

from press_api_spec.proxy_service_v1.base import Endpoint, EndpointGroup
from press_api_spec.proxy_service_v1.endpoints.action import *  # noqa: F401,F403
from press_api_spec.proxy_service_v1.endpoints.action import actions
from press_api_spec.proxy_service_v1.endpoints.domain import *  # noqa: F401,F403
from press_api_spec.proxy_service_v1.endpoints.domain import domains
from press_api_spec.proxy_service_v1.endpoints.health import *  # noqa: F401,F403
from press_api_spec.proxy_service_v1.endpoints.health import health
from press_api_spec.proxy_service_v1.endpoints.redirect import *  # noqa: F401,F403
from press_api_spec.proxy_service_v1.endpoints.redirect import redirects
from press_api_spec.proxy_service_v1.endpoints.route import *  # noqa: F401,F403
from press_api_spec.proxy_service_v1.endpoints.route import routes

ALL_GROUPS: list[EndpointGroup] = [domains, redirects, routes, health, actions]
ALL_ENDPOINTS: list[Endpoint[Any, Any]] = [ep for group in ALL_GROUPS for ep in group]
