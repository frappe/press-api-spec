from __future__ import annotations

from typing import Any

from press_api_spec.bench_manager_service_v1.endpoints.app import *  # noqa: F401,F403
from press_api_spec.bench_manager_service_v1.endpoints.app import AppGroup
from press_api_spec.bench_manager_service_v1.endpoints.bench import *  # noqa: F401,F403
from press_api_spec.bench_manager_service_v1.endpoints.bench import BenchGroup
from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup

ALL_GROUPS: list[EndpointGroup] = [AppGroup, BenchGroup]
ALL_ENDPOINTS: list[Endpoint[Any, Any]] = [ep for group in ALL_GROUPS for ep in group]
