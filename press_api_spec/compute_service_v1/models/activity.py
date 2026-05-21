from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

from press_api_spec.compute_service_v1.base import Paginated, PaginationParams

__all__ = [
    "ActivityLogResourceType",
    "ActivityLogSource",
    "ActivityLogEntry",
    "ListActivityLogsQuery",
    "ListActivityLogsResponse",
]


class ActivityLogResourceType(str, Enum):
    STACK = "stack"
    CONTAINER = "container"
    VOLUME = "volume"
    NETWORK = "network"
    SNAPSHOT = "snapshot"


class ActivityLogSource(str, Enum):
    USER = "user"
    AGENT = "agent"
    VOLUME_AGENT = "volume-agent"
    CONTROL_PLANE = "control-plane"
    SYSTEM = "system"


class ActivityLogEntry(BaseModel):
    id: str
    resource_type: ActivityLogResourceType
    resource_id: str
    source: ActivityLogSource
    actor: str | None = None
    message: str
    metadata: dict | None = None
    created_at_unix: int = Field(
        description="UTC timestamp in seconds since epoch", examples=[1736935200]
    )


class ListActivityLogsQuery(PaginationParams):
    source: ActivityLogSource | None = None


ListActivityLogsResponse = Paginated[ActivityLogEntry]
