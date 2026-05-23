from __future__ import annotations

from press_api_spec.proxy_service_v1.base import Endpoint, EndpointGroup
from press_api_spec.proxy_service_v1.endpoints.domain import *  # noqa: F401,F403
from press_api_spec.proxy_service_v1.endpoints.domain import DomainGroup
from press_api_spec.proxy_service_v1.endpoints.health import *  # noqa: F401,F403
from press_api_spec.proxy_service_v1.endpoints.health import HealthGroup
from press_api_spec.proxy_service_v1.endpoints.redirect import *  # noqa: F401,F403
from press_api_spec.proxy_service_v1.endpoints.redirect import RedirectGroup
from press_api_spec.proxy_service_v1.endpoints.route import *  # noqa: F401,F403
from press_api_spec.proxy_service_v1.endpoints.route import RouteGroup
from press_api_spec.proxy_service_v1.endpoints.root_domain import *  # noqa: F401,F403
from press_api_spec.proxy_service_v1.endpoints.root_domain import RootDomainGroup

ALL_GROUPS: list[EndpointGroup] = [
    DomainGroup,
    RedirectGroup,
    RouteGroup,
    HealthGroup,
    RootDomainGroup,
]
ALL_ENDPOINTS: list[type[Endpoint]] = [ep for group in ALL_GROUPS for ep in group]
