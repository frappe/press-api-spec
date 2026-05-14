from __future__ import annotations

from typing import Any

from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup
from press_api_spec.compute_service_v1.endpoints.action import *  # noqa: F401,F403
from press_api_spec.compute_service_v1.endpoints.action import actions
from press_api_spec.compute_service_v1.endpoints.container import *  # noqa: F401,F403
from press_api_spec.compute_service_v1.endpoints.container import containers
from press_api_spec.compute_service_v1.endpoints.health import *  # noqa: F401,F403
from press_api_spec.compute_service_v1.endpoints.health import health
from press_api_spec.compute_service_v1.endpoints.snapshot import *  # noqa: F401,F403
from press_api_spec.compute_service_v1.endpoints.snapshot import snapshots
from press_api_spec.compute_service_v1.endpoints.stack import *  # noqa: F401,F403
from press_api_spec.compute_service_v1.endpoints.stack import stacks
from press_api_spec.compute_service_v1.endpoints.volume import *  # noqa: F401,F403
from press_api_spec.compute_service_v1.endpoints.volume import volumes

ALL_GROUPS: list[EndpointGroup] = [stacks, containers, volumes, snapshots, health, actions]
ALL_ENDPOINTS: list[Endpoint[Any, Any]] = [ep for group in ALL_GROUPS for ep in group]
