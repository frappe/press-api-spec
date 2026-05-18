from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

from press_api_spec.compute_service_v1.base import (
    ActionRecord,
    EmptyResponse,
    Paginated,
    PaginationParams,
)
from press_api_spec.compute_service_v1.models.container import CreateContainerRequest

__all__ = [
    "Runtime",
    "NetworkingMode",
    "StackStatus",
    "StackResources",
    "Stack",
    "CreateStackRequest",
    "CreateStackResponse",
    "GetStackResponse",
    "ListStacksQuery",
    "ListStacksResponse",
    "UpdateStackRequest",
    "UpdateStackResponse",
    "DeleteStackResponse",
    "ResizeStackRequest",
    "ResizeStackResponse",
    "StackActionResponse",
]


class Runtime(str, Enum):
    CONTAINER = "container"


class NetworkingMode(str, Enum):
    ISOLATED = "isolated"
    HOST = "host"


class StackStatus(str, Enum):
    PENDING = "pending"
    CREATING = "creating"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    STARTING = "starting"
    RESTARTING = "restarting"
    RESIZING = "resizing"
    TERMINATING = "terminating"
    TERMINATED = "terminated"
    ERROR = "error"


class StackResources(BaseModel):
    memory_low: float | None = Field(default=None, examples=[1.0, 2.0])
    memory_high: float | None = Field(default=None, examples=[2.0, 4.0])
    memory_max: float | None = Field(default=None, examples=[2.0, 8.0])
    cpu_quota: float | None = Field(default=None, examples=[0.5, 1.0, 2.0])


class Stack(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "stack_abc123",
                    "name": "my-app",
                    "description": "Production API stack",
                    "status": "running",
                    "runtime": "container",
                    "networking": "isolated",
                    "resources": {
                        "memory_low": 1.0,
                        "memory_high": 2.0,
                        "memory_max": 4.0,
                        "cpu_quota": 1.0,
                    },
                    "created_at_unix": 1736935200,
                    "updated_at_unix": 1736942400,
                }
            ]
        }
    )

    # Server-generated unique identifier (immutable)
    id: str = Field(description="Server-generated unique identifier")
    # User-provided identifier, set at creation only (immutable after creation)
    name: str = Field(examples=["my-app", "production-api"], description="User-provided identifier, set at creation only")
    # Arbitrary user-provided description (modifiable)
    description: str | None = Field(default=None, examples=["Production API stack"], description="Arbitrary user-provided description")
    status: StackStatus = StackStatus.PENDING
    runtime: Runtime = Runtime.CONTAINER
    networking: NetworkingMode = NetworkingMode.ISOLATED
    resources: StackResources = StackResources()
    created_at_unix: int
    updated_at_unix: int


class CreateStackRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "my-app",
                    "description": "Production API stack",
                    "containers": [{"image": "nginx:latest", "resources": {"memory_max": 1.0}}],
                    "runtime": "container",
                    "networking": "isolated",
                }
            ]
        }
    )

    name: str = Field(examples=["my-app", "production-api"])
    description: str | None = Field(default=None, examples=["Production API stack"])
    containers: list[CreateContainerRequest] = []
    runtime: Runtime = Runtime.CONTAINER
    networking: NetworkingMode = NetworkingMode.ISOLATED


class CreateStackResponse(BaseModel):
    stack: Stack


class ListStacksQuery(PaginationParams):
    status: StackStatus | None = None
    name: str | None = Field(default=None, examples=["my-app"])


ListStacksResponse = Paginated[Stack]


class GetStackResponse(BaseModel):
    stack: Stack


class UpdateStackRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"description": "Updated description"}]
        }
    )

    description: str | None = Field(default=None, examples=["Updated description"])


class UpdateStackResponse(BaseModel):
    stack: Stack


DeleteStackResponse = EmptyResponse


class ResizeStackRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "resources": {
                        "memory_low": 2.0,
                        "memory_high": 4.0,
                        "memory_max": 8.0,
                        "cpu_quota": 2.0,
                    }
                }
            ]
        }
    )

    resources: StackResources


class ResizeStackResponse(BaseModel):
    stack: Stack
    action: ActionRecord


class StackActionResponse(BaseModel):
    stack: Stack
    action: ActionRecord
