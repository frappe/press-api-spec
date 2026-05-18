from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

from press_api_spec.compute_service_v1.base import (
    ActionRecord,
    EmptyResponse,
    Paginated,
    PaginationParams,
)
from press_api_spec.compute_service_v1.models.volume import VolumeMountStatus

__all__ = [
    "ContainerStatus",
    "ContainerResources",
    "ContainerVolumeMount",
    "Container",
    "CreateContainerRequest",
    "CreateContainerResponse",
    "GetContainerResponse",
    "ListContainersQuery",
    "ListContainersResponse",
    "UpdateContainerRequest",
    "UpdateContainerResponse",
    "DeleteContainerResponse",
    "ResizeContainerRequest",
    "ResizeContainerResponse",
    "ContainerActionResponse",
]


class ContainerStatus(str, Enum):
    PENDING = "pending"
    CREATING = "creating"
    RUNNING = "running"
    UPDATING = "updating"
    STOPPING = "stopping"
    STOPPED = "stopped"
    STARTING = "starting"
    RESTARTING = "restarting"
    RESIZING = "resizing"
    TERMINATING = "terminating"
    TERMINATED = "terminated"
    ERROR = "error"


class ContainerVolumeMount(BaseModel):
    volume_id: str = Field(examples=["vol_abc123"])
    mountpoint: str = Field(examples=["/data", "/var/lib/postgresql"])
    status: VolumeMountStatus = VolumeMountStatus.ATTACHED


class ContainerResources(BaseModel):
    memory_low: float | None = Field(default=None, examples=[1.0, 2.0])
    memory_high: float | None = Field(default=None, examples=[2.0, 4.0])
    memory_max: float | None = Field(default=None, examples=[2.0, 8.0])


class Container(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "ctr_def456",
                    "stack_id": "stack_abc123",
                    "name": "web",
                    "image": "nginx:latest",
                    "resources": {"memory_max": 1.0},
                    "status": "running",
                    "command": None,
                    "env": {"NODE_ENV": "production"},
                    "volume_mounts": [
                        {"volume_id": "vol_abc123", "mountpoint": "/data", "status": "attached"}
                    ],
                    "created_at_unix": 1736935200,
                    "updated_at_unix": 1736942400,
                }
            ]
        }
    )

    # Server-generated unique identifier (immutable)
    id: str = Field(description="Server-generated unique identifier")
    # Reference to parent stack (immutable)
    stack_id: str = Field(description="Reference to parent stack")
    # User-provided identifier, set at creation only (immutable after creation)
    name: str = Field(
        examples=["web", "db"], description="User-provided identifier, set at creation only"
    )
    # Container image reference (modifiable)
    image: str = Field(
        examples=["nginx:latest", "node:20-alpine"], description="Container image reference"
    )
    resources: ContainerResources
    status: ContainerStatus = ContainerStatus.PENDING
    # Override entrypoint command (modifiable)
    command: str | None = Field(
        default=None,
        examples=["npm start", "python app.py"],
        description="Override entrypoint command",
    )
    # Environment variables (modifiable)
    env: dict[str, str] = Field(default_factory=dict, description="Environment variables")
    volume_mounts: list[ContainerVolumeMount] = []
    created_at_unix: int
    updated_at_unix: int


class CreateContainerRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "image": "nginx:latest",
                    "name": "web",
                    "resources": {"memory_max": 1.0},
                    "command": None,
                    "env": {"NODE_ENV": "production"},
                    "volume_mounts": [
                        {"volume_id": "vol_abc123", "mountpoint": "/data", "status": "attached"}
                    ],
                }
            ]
        }
    )

    image: str = Field(examples=["nginx:latest", "node:20-alpine"])
    name: str = Field(examples=["web", "db"])
    resources: ContainerResources = ContainerResources()
    command: str | None = Field(default=None, examples=["npm start", "python app.py"])
    env: dict[str, str] = {}
    volume_mounts: list[ContainerVolumeMount] = []


class CreateContainerResponse(BaseModel):
    container: Container


class ListContainersQuery(PaginationParams):
    status: ContainerStatus | None = None


ListContainersResponse = Paginated[Container]


class GetContainerResponse(BaseModel):
    container: Container


class UpdateContainerRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "image": "nginx:1.27",
                    "command": "nginx -g 'daemon off;'",
                    "env": {"NODE_ENV": "production", "LOG_LEVEL": "info"},
                }
            ]
        }
    )

    image: str | None = Field(default=None, examples=["nginx:1.27", "node:20-alpine"])
    command: str | None = Field(default=None, examples=["npm start", "python app.py"])
    env: dict[str, str] | None = None


class UpdateContainerResponse(BaseModel):
    container: Container


DeleteContainerResponse = EmptyResponse


class ResizeContainerRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"resources": {"memory_low": 2.0, "memory_high": 4.0, "memory_max": 8.0}}]
        }
    )

    resources: ContainerResources


class ResizeContainerResponse(BaseModel):
    container: Container
    action: ActionRecord


class ContainerActionResponse(BaseModel):
    container: Container
    action: ActionRecord
