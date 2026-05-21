from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

from press_api_spec.compute_service_v1.base import EmptyResponse, Paginated, PaginationParams
from press_api_spec.compute_service_v1.models.container import Container, CreateContainerRequest

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
    HOST = "host"
    OVERLAY = "overlay"


class StackStatus(str, Enum):
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
                    "name": "production-api",
                    "description": "Production web application stack with database and cache",
                    "status": "running",
                    "runtime": "container",
                    "networking": "overlay",
                    "network_id": "net_abc123",
                    "resources": {
                        "memory_low": 4.0,
                        "memory_high": 8.0,
                        "memory_max": 16.0,
                        "cpu_quota": 4.0,
                    },
                    "created_at_unix": 1736935200,
                    "updated_at_unix": 1736942400,
                },
            ]
        }
    )

    id: str = Field(description="Server-generated unique identifier")
    name: str = Field(
        examples=["my-app", "production-api"],
        description="User-provided identifier, set at creation only",
    )
    description: str | None = Field(
        default=None,
        examples=["Production API stack"],
        description="Arbitrary user-provided description",
    )
    status: StackStatus = StackStatus.PENDING
    runtime: Runtime = Runtime.CONTAINER
    networking: NetworkingMode = NetworkingMode.HOST
    network_id: str | None = Field(
        default=None,
        examples=["net_abc123"],
        description="Network ID for overlay mode; required when networking is 'overlay'",
    )
    resources: StackResources = StackResources()
    containers: list[Container] = Field(default_factory=list)
    created_at_unix: int
    updated_at_unix: int


class CreateStackRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "production-api",
                    "description": "Production web application stack with database and cache",
                    "containers": [
                        {
                            "name": "web",
                            "image": "nginx:1.27-alpine",
                            "command": None,
                            "env": {
                                "NODE_ENV": "production",
                                "PORT": "8080",
                                "API_URL": "http://api:3000",
                            },
                            "resources": {
                                "memory_low": 0.5,
                                "memory_high": 1.0,
                                "memory_max": 2.0,
                            },
                            "volume_mounts": [
                                {"volume_id": "vol_logs", "mountpoint": "/var/log/nginx"},
                                {"volume_id": "vol_certs", "mountpoint": "/etc/nginx/ssl"},
                            ],
                        },
                        {
                            "name": "api",
                            "image": "node:20-alpine",
                            "command": "npm start",
                            "env": {
                                "NODE_ENV": "production",
                                "DATABASE_URL": "postgres://app:secret@db:5432/appdb",
                                "REDIS_URL": "redis://cache:6379",
                                "PORT": "3000",
                            },
                            "resources": {
                                "memory_low": 1.0,
                                "memory_high": 2.0,
                                "memory_max": 4.0,
                            },
                            "volume_mounts": [],
                        },
                        {
                            "name": "db",
                            "image": "postgres:16",
                            "command": "postgres -c max_connections=200 -c shared_buffers=1GB",
                            "env": {
                                "POSTGRES_DB": "appdb",
                                "POSTGRES_USER": "app",
                                "POSTGRES_PASSWORD": "secret",
                            },
                            "resources": {
                                "memory_low": 2.0,
                                "memory_high": 4.0,
                                "memory_max": 8.0,
                            },
                            "volume_mounts": [
                                {
                                    "volume_id": "vol_pgdata",
                                    "mountpoint": "/var/lib/postgresql/data",
                                },
                            ],
                        },
                        {
                            "name": "cache",
                            "image": "redis:7-alpine",
                            "command": "redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru",
                            "env": {},
                            "resources": {
                                "memory_low": 0.5,
                                "memory_high": 1.0,
                                "memory_max": 1.0,
                            },
                            "volume_mounts": [],
                        },
                    ],
                    "runtime": "container",
                    "networking": "overlay",
                    "network_id": "net_abc123",
                },
            ]
        }
    )

    name: str = Field(examples=["my-app", "production-api"])
    description: str | None = Field(default=None, examples=["Production API stack"])
    containers: list[CreateContainerRequest] = []
    runtime: Runtime = Runtime.CONTAINER
    networking: NetworkingMode = NetworkingMode.HOST
    network_id: str | None = Field(
        default=None,
        examples=["net_abc123"],
        description="Network ID for overlay mode; required when networking is 'overlay'",
    )


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
        json_schema_extra={"examples": [{"description": "Updated description"}]}
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


class StackActionResponse(BaseModel):
    stack: Stack
