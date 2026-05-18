from __future__ import annotations

from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup
from press_api_spec.compute_service_v1.endpoints.agent_sync import *  # noqa: F401,F403
from press_api_spec.compute_service_v1.endpoints.agent_sync import AgentSyncGroup
from press_api_spec.compute_service_v1.endpoints.container import *  # noqa: F401,F403
from press_api_spec.compute_service_v1.endpoints.container import ContainerGroup
from press_api_spec.compute_service_v1.endpoints.health import *  # noqa: F401,F403
from press_api_spec.compute_service_v1.endpoints.health import HealthGroup
from press_api_spec.compute_service_v1.endpoints.network import *  # noqa: F401,F403
from press_api_spec.compute_service_v1.endpoints.network import NetworkGroup
from press_api_spec.compute_service_v1.endpoints.snapshot import *  # noqa: F401,F403
from press_api_spec.compute_service_v1.endpoints.snapshot import SnapshotGroup
from press_api_spec.compute_service_v1.endpoints.stack import *  # noqa: F401,F403
from press_api_spec.compute_service_v1.endpoints.stack import StackGroup
from press_api_spec.compute_service_v1.endpoints.volume import *  # noqa: F401,F403
from press_api_spec.compute_service_v1.endpoints.volume import VolumeGroup

ALL_GROUPS: list[EndpointGroup] = [
    HealthGroup,
    AgentSyncGroup,
    NetworkGroup,
    StackGroup,
    ContainerGroup,
    VolumeGroup,
    SnapshotGroup,
]
ALL_ENDPOINTS: list[type[Endpoint]] = [ep for group in ALL_GROUPS for ep in group]
