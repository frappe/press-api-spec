"""Agent sync models — reconciliation between control plane and node agents.

Versioning model
================

Two versioning fields work together to enable efficient and granular reconciliation:

revision (on AgentNodeSpec)
    Global snapshot version for the entire desired state of a node.
    Monotonically increasing; incremented whenever any object on the node changes.
    The agent compares this against the revision it last applied and can skip the
    entire reconcile loop if unchanged.  When the agent posts a status report it
    includes `spec_revision` so the control plane knows which snapshot the report
    corresponds to.

version (on each Agent*Spec)
    Per-object version.  Incremented only when that specific object changes.
    Lets the control plane know exactly which objects the agent has applied and
    which are still pending, even when a single spec revision touches multiple
    objects.

applied_version (on each Agent*StatusReport)
    The version of the spec object that the agent has successfully applied.
    The control plane compares `spec.version` vs `report.applied_version` per
    object to determine reconciliation state.

Example flow:
    1. Control plane sends spec revision=42 (network v1, stack v3, volume v2).
    2. Agent polls, sees revision 42 != last_seen 41, starts reconcile.
    3. Agent applies network v1 and stack v3 but volume v2 is still provisioning.
    4. Agent reports: spec_revision=42, networks=[applied_version=1],
       stacks=[applied_version=3], volumes=[applied_version=1] (still on old).
    5. Control plane sees volume v2 is pending, knows not to mark it as applied.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from press_api_spec.compute_service_v1.base import EmptyResponse
from press_api_spec.compute_service_v1.models.container import (
    ContainerResources,
    ContainerStatus,
    ContainerVolumeMount,
)
from press_api_spec.compute_service_v1.models.stack import (
    NetworkingMode,
    StackResources,
    StackStatus,
)
from press_api_spec.compute_service_v1.models.volume import VolumeStatus

__all__ = [
    "AgentDesiredStatus",
    "AgentNetworkSpec",
    "AgentVolumeSpec",
    "AgentDesiredContainerSpec",
    "AgentDesiredStackSpec",
    "AgentNodeSpec",
    "GetAgentNodeSpecResponse",
    "AgentNetworkStatusReport",
    "AgentVolumeStatusReport",
    "AgentContainerStatusReport",
    "AgentStackStatusReport",
    "AgentResourceMetrics",
    "AgentResourceReport",
    "ReportAgentNodeStatusRequest",
    "ReportAgentNodeStatusResponse",
]


class AgentDesiredStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    DELETED = "deleted"


# ---------------------------------------------------------------------------
# Desired state — control plane → agent (GET /api/agent/spec)
# ---------------------------------------------------------------------------


class AgentNetworkSpec(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "net_abc123",
                    "name": "production-overlay",
                    "cidr": "10.0.0.0/16",
                    "gateway_ip": "10.0.0.1",
                    "version": 1,
                },
                {
                    "id": "net_def456",
                    "name": "staging-overlay",
                    "cidr": "10.1.0.0/16",
                    "gateway_ip": "10.1.0.1",
                    "version": 3,
                },
            ]
        }
    )

    id: str = Field(description="Network ID assigned by the control plane")
    name: str = Field(examples=["production-overlay", "staging-overlay"])
    cidr: str = Field(examples=["10.0.0.0/16", "10.1.0.0/16"])
    gateway_ip: str = Field(examples=["10.0.0.1", "10.1.0.1"])
    version: int = Field(
        description="Monotonically increasing version; incremented on each change",
        examples=[1, 3],
    )


class AgentVolumeSpec(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "vol_pgdata",
                    "name": "postgres-data",
                    "size_gb": 50.0,
                    "mountpoint": "/var/lib/postgresql/data",
                    "status": "in-use",
                    "version": 1,
                },
                {
                    "id": "vol_logs",
                    "name": "app-logs",
                    "size_gb": 10.0,
                    "mountpoint": "/var/log/app",
                    "status": "available",
                    "version": 2,
                },
            ]
        }
    )

    id: str = Field(description="Volume ID assigned by the control plane")
    name: str = Field(examples=["postgres-data", "app-logs"])
    size_gb: float = Field(examples=[10.0, 50.0, 100.0])
    mountpoint: str | None = Field(default=None, examples=["/var/lib/postgresql/data", "/data"])
    status: VolumeStatus = Field(
        default=VolumeStatus.AVAILABLE,
        description="Desired state of the volume",
    )
    version: int = Field(
        description="Monotonically increasing version; incremented on each change",
        examples=[1, 2],
    )


class AgentDesiredContainerSpec(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "ctr_a1b2c3",
                    "name": "web",
                    "image": "nginx:1.27-alpine",
                    "command": None,
                    "env": {"NODE_ENV": "production", "PORT": "8080"},
                    "resources": {"memory_low": 0.5, "memory_high": 1.0, "memory_max": 2.0},
                    "volume_mounts": [
                        {
                            "volume_id": "vol_logs",
                            "mountpoint": "/var/log/nginx",
                            "status": "attached",
                        }
                    ],
                    "version": 1,
                },
                {
                    "id": "ctr_d4e5f6",
                    "name": "db",
                    "image": "postgres:16",
                    "command": "postgres -c max_connections=200",
                    "env": {"POSTGRES_DB": "appdb", "POSTGRES_USER": "app"},
                    "resources": {"memory_low": 2.0, "memory_high": 4.0, "memory_max": 8.0},
                    "volume_mounts": [
                        {
                            "volume_id": "vol_pgdata",
                            "mountpoint": "/var/lib/postgresql/data",
                            "status": "attached",
                        }
                    ],
                    "version": 5,
                },
            ]
        }
    )

    id: str = Field(description="Container ID assigned by the control plane")
    name: str = Field(examples=["web", "db"])
    image: str = Field(examples=["nginx:1.27-alpine", "postgres:16"])
    command: str | None = Field(
        default=None, examples=["npm start", "postgres -c max_connections=200"]
    )
    env: dict[str, str] = Field(default_factory=dict)
    resources: ContainerResources = ContainerResources()
    volume_mounts: list[ContainerVolumeMount] = []
    version: int = Field(
        description="Monotonically increasing version; incremented on each change",
        examples=[1, 5],
    )


class AgentDesiredStackSpec(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "stack_abc123",
                    "name": "production-api",
                    "desired_status": "running",
                    "networking": "overlay",
                    "network_id": "net_abc123",
                    "resources": {
                        "memory_low": 2.0,
                        "memory_high": 4.0,
                        "memory_max": 8.0,
                        "cpu_quota": 2.0,
                    },
                    "containers": [
                        {
                            "id": "ctr_a1b2c3",
                            "name": "web",
                            "image": "nginx:1.27-alpine",
                            "command": None,
                            "env": {"NODE_ENV": "production"},
                            "resources": {"memory_max": 2.0},
                            "volume_mounts": [
                                {
                                    "volume_id": "vol_logs",
                                    "mountpoint": "/var/log/nginx",
                                    "status": "attached",
                                }
                            ],
                            "version": 1,
                        },
                        {
                            "id": "ctr_d4e5f6",
                            "name": "db",
                            "image": "postgres:16",
                            "env": {"POSTGRES_DB": "appdb"},
                            "resources": {"memory_max": 4.0},
                            "volume_mounts": [
                                {
                                    "volume_id": "vol_pgdata",
                                    "mountpoint": "/var/lib/postgresql/data",
                                    "status": "attached",
                                }
                            ],
                            "version": 3,
                        },
                    ],
                    "version": 1,
                },
                {
                    "id": "stack_def456",
                    "name": "worker",
                    "desired_status": "running",
                    "networking": "host",
                    "network_id": None,
                    "resources": {
                        "memory_low": 1.0,
                        "memory_high": 2.0,
                        "memory_max": 4.0,
                        "cpu_quota": 1.0,
                    },
                    "containers": [
                        {
                            "id": "ctr_g7h8i9",
                            "name": "worker",
                            "image": "node:20-alpine",
                            "command": "npm run worker",
                            "env": {"REDIS_URL": "redis://cache:6379"},
                            "resources": {"memory_max": 2.0},
                            "volume_mounts": [],
                            "version": 2,
                        },
                    ],
                    "version": 4,
                },
            ]
        }
    )

    id: str = Field(description="Stack ID assigned by the control plane")
    name: str = Field(examples=["production-api", "worker"])
    desired_status: AgentDesiredStatus
    networking: NetworkingMode = NetworkingMode.HOST
    network_id: str | None = Field(
        default=None,
        examples=["net_abc123"],
        description="Network ID for overlay mode; required when networking is 'overlay'",
    )
    resources: StackResources = StackResources()
    containers: list[AgentDesiredContainerSpec] = []
    version: int = Field(
        description="Monotonically increasing version; incremented on each change",
        examples=[1, 4],
    )


class AgentNodeSpec(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "node_id": "node_us-east-1_001",
                    "revision": 42,
                    "networks": [
                        {
                            "id": "net_abc123",
                            "name": "production-overlay",
                            "cidr": "10.0.0.0/16",
                            "gateway_ip": "10.0.0.1",
                            "version": 1,
                        },
                        {
                            "id": "net_def456",
                            "name": "staging-overlay",
                            "cidr": "10.1.0.0/16",
                            "gateway_ip": "10.1.0.1",
                            "version": 3,
                        },
                    ],
                    "volumes": [
                        {
                            "id": "vol_pgdata",
                            "name": "postgres-data",
                            "size_gb": 50.0,
                            "mountpoint": "/var/lib/postgresql/data",
                            "status": "in-use",
                            "version": 1,
                        },
                        {
                            "id": "vol_logs",
                            "name": "app-logs",
                            "size_gb": 10.0,
                            "mountpoint": "/var/log/app",
                            "status": "in-use",
                            "version": 2,
                        },
                    ],
                    "stacks": [
                        {
                            "id": "stack_abc123",
                            "name": "production-api",
                            "desired_status": "running",
                            "networking": "overlay",
                            "network_id": "net_abc123",
                            "resources": {
                                "memory_low": 2.0,
                                "memory_high": 4.0,
                                "memory_max": 8.0,
                                "cpu_quota": 2.0,
                            },
                            "containers": [
                                {
                                    "id": "ctr_a1b2c3",
                                    "name": "web",
                                    "image": "nginx:1.27-alpine",
                                    "env": {"NODE_ENV": "production"},
                                    "resources": {"memory_max": 2.0},
                                    "volume_mounts": [
                                        {
                                            "volume_id": "vol_logs",
                                            "mountpoint": "/var/log/nginx",
                                            "status": "attached",
                                        }
                                    ],
                                    "version": 1,
                                },
                                {
                                    "id": "ctr_d4e5f6",
                                    "name": "db",
                                    "image": "postgres:16",
                                    "env": {"POSTGRES_DB": "appdb"},
                                    "resources": {"memory_max": 4.0},
                                    "volume_mounts": [
                                        {
                                            "volume_id": "vol_pgdata",
                                            "mountpoint": "/var/lib/postgresql/data",
                                            "status": "attached",
                                        }
                                    ],
                                    "version": 3,
                                },
                            ],
                            "version": 1,
                        },
                        {
                            "id": "stack_def456",
                            "name": "worker",
                            "desired_status": "running",
                            "networking": "host",
                            "network_id": None,
                            "resources": {
                                "memory_low": 1.0,
                                "memory_high": 2.0,
                                "memory_max": 4.0,
                                "cpu_quota": 1.0,
                            },
                            "containers": [
                                {
                                    "id": "ctr_g7h8i9",
                                    "name": "worker",
                                    "image": "node:20-alpine",
                                    "command": "npm run worker",
                                    "env": {"REDIS_URL": "redis://cache:6379"},
                                    "resources": {"memory_max": 2.0},
                                    "volume_mounts": [],
                                    "version": 2,
                                },
                            ],
                            "version": 4,
                        },
                    ],
                }
            ]
        }
    )

    node_id: str = Field(description="Node this spec is scoped to")
    revision: int = Field(
        description="Monotonically increasing global revision number; agent can skip reconcile if unchanged. Each object also carries its own version for granular tracking.",
        examples=[42],
    )
    networks: list[AgentNetworkSpec] = []
    volumes: list[AgentVolumeSpec] = []
    stacks: list[AgentDesiredStackSpec] = []


class GetAgentNodeSpecResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "spec": {
                        "node_id": "node_us-east-1_001",
                        "revision": 42,
                        "networks": [
                            {
                                "id": "net_abc123",
                                "name": "production-overlay",
                                "cidr": "10.0.0.0/16",
                                "gateway_ip": "10.0.0.1",
                                "version": 1,
                            }
                        ],
                        "volumes": [
                            {
                                "id": "vol_pgdata",
                                "name": "postgres-data",
                                "size_gb": 50.0,
                                "mountpoint": "/var/lib/postgresql/data",
                                "status": "in-use",
                                "version": 1,
                            }
                        ],
                        "stacks": [
                            {
                                "id": "stack_abc123",
                                "name": "production-api",
                                "desired_status": "running",
                                "networking": "overlay",
                                "network_id": "net_abc123",
                                "resources": {
                                    "memory_low": 2.0,
                                    "memory_high": 4.0,
                                    "memory_max": 8.0,
                                    "cpu_quota": 2.0,
                                },
                                "containers": [
                                    {
                                        "id": "ctr_a1b2c3",
                                        "name": "web",
                                        "image": "nginx:1.27-alpine",
                                        "env": {"NODE_ENV": "production"},
                                        "resources": {"memory_max": 2.0},
                                        "volume_mounts": [
                                            {
                                                "volume_id": "vol_logs",
                                                "mountpoint": "/var/log/nginx",
                                                "status": "attached",
                                            }
                                        ],
                                        "version": 1,
                                    },
                                    {
                                        "id": "ctr_d4e5f6",
                                        "name": "db",
                                        "image": "postgres:16",
                                        "env": {"POSTGRES_DB": "appdb"},
                                        "resources": {"memory_max": 4.0},
                                        "volume_mounts": [
                                            {
                                                "volume_id": "vol_pgdata",
                                                "mountpoint": "/var/lib/postgresql/data",
                                                "status": "attached",
                                            }
                                        ],
                                        "version": 3,
                                    },
                                ],
                                "version": 1,
                            }
                        ],
                    }
                }
            ]
        }
    )

    spec: AgentNodeSpec


# ---------------------------------------------------------------------------
# Status report — agent → control plane (POST /api/agent/report)
# ---------------------------------------------------------------------------


class AgentNetworkStatusReport(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "network_id": "net_abc123",
                    "observed_status": "available",
                    "message": None,
                    "last_error": None,
                    "applied_version": 1,
                },
                {
                    "network_id": "net_def456",
                    "observed_status": "error",
                    "message": "Failed to create overlay network",
                    "last_error": "address space already in use",
                    "applied_version": 3,
                },
            ]
        }
    )

    network_id: str
    observed_status: str = Field(
        examples=["creating", "available", "error", "deleting"],
        description="Observed state of the network on this node",
    )
    message: str | None = None
    last_error: str | None = None
    applied_version: int = Field(
        description="Version of the network spec that was applied",
        examples=[1, 3],
    )


class AgentVolumeStatusReport(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "volume_id": "vol_pgdata",
                    "observed_status": "in-use",
                    "size_gb": 50.0,
                    "iops": 3000,
                    "throughput_mbps": 125,
                    "message": None,
                    "last_error": None,
                    "applied_version": 1,
                },
                {
                    "volume_id": "vol_logs",
                    "observed_status": "error",
                    "size_gb": 10.0,
                    "iops": 3000,
                    "throughput_mbps": 125,
                    "message": "Volume mount failed",
                    "last_error": "device not found",
                    "applied_version": 2,
                },
            ]
        }
    )

    volume_id: str
    observed_status: VolumeStatus = Field(
        description="Observed state of the volume on this node",
    )
    size_gb: float | None = Field(default=None, examples=[10.0, 50.0, 100.0])
    iops: int | None = Field(default=None, examples=[3000, 16000])
    throughput_mbps: int | None = Field(default=None, examples=[125, 500])
    message: str | None = None
    last_error: str | None = None
    applied_version: int = Field(
        description="Version of the volume spec that was applied",
        examples=[1, 2],
    )


class AgentContainerStatusReport(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "container_id": "ctr_a1b2c3",
                    "observed_status": "running",
                    "runtime_id": "sha256:abc123def456",
                    "message": None,
                    "last_error": None,
                    "applied_version": 1,
                },
                {
                    "container_id": "ctr_d4e5f6",
                    "observed_status": "error",
                    "runtime_id": "sha256:789ghi012jkl",
                    "message": "Container exited with code 1",
                    "last_error": "FATAL: too many connections for role 'app'",
                    "applied_version": 5,
                },
            ]
        }
    )

    container_id: str
    observed_status: ContainerStatus
    runtime_id: str | None = Field(
        default=None,
        description="Underlying container runtime ID (e.g. Docker container ID)",
    )
    message: str | None = None
    last_error: str | None = None
    applied_version: int = Field(
        description="Version of the container spec that was applied",
        examples=[1, 5],
    )


class AgentStackStatusReport(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "stack_id": "stack_abc123",
                    "observed_status": "running",
                    "message": None,
                    "last_error": None,
                    "containers": [
                        {
                            "container_id": "ctr_a1b2c3",
                            "observed_status": "running",
                            "runtime_id": "sha256:abc123def456",
                            "message": None,
                            "last_error": None,
                            "applied_version": 1,
                        },
                        {
                            "container_id": "ctr_d4e5f6",
                            "observed_status": "running",
                            "runtime_id": "sha256:789ghi012jkl",
                            "message": None,
                            "last_error": None,
                            "applied_version": 3,
                        },
                    ],
                    "applied_version": 1,
                },
                {
                    "stack_id": "stack_def456",
                    "observed_status": "error",
                    "message": "Worker container crashed on startup",
                    "last_error": "Error: connect ECONNREFUSED 127.0.0.1:6379",
                    "containers": [
                        {
                            "container_id": "ctr_g7h8i9",
                            "observed_status": "error",
                            "runtime_id": None,
                            "message": "Container failed to start",
                            "last_error": "Error: connect ECONNREFUSED 127.0.0.1:6379",
                            "applied_version": 2,
                        },
                    ],
                    "applied_version": 4,
                },
            ]
        }
    )

    stack_id: str
    observed_status: StackStatus
    message: str | None = None
    last_error: str | None = None
    containers: list[AgentContainerStatusReport] = []
    applied_version: int = Field(
        description="Version of the stack spec that was applied",
        examples=[1, 4],
    )


class AgentResourceMetrics(BaseModel):
    total: float = Field(examples=[16.0, 8.0, 100.0])
    available: float = Field(examples=[12.5, 6.0, 85.3])
    allocated: float = Field(examples=[3.5, 2.0, 14.7])


class AgentResourceReport(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "memory_gb": {"total": 16.0, "available": 12.5, "allocated": 3.5},
                    "cpu_cores": {"total": 8.0, "available": 6.0, "allocated": 2.0},
                    "disk_gb": {"total": 100.0, "available": 85.3, "allocated": 14.7},
                }
            ]
        }
    )

    memory_gb: AgentResourceMetrics | None = None
    cpu_cores: AgentResourceMetrics | None = None
    disk_gb: AgentResourceMetrics | None = None


class ReportAgentNodeStatusRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "networks": [
                        {
                            "network_id": "net_abc123",
                            "observed_status": "available",
                            "message": None,
                            "last_error": None,
                            "applied_version": 1,
                        }
                    ],
                    "volumes": [
                        {
                            "volume_id": "vol_pgdata",
                            "observed_status": "in-use",
                            "size_gb": 50.0,
                            "iops": 3000,
                            "throughput_mbps": 125,
                            "message": None,
                            "last_error": None,
                            "applied_version": 1,
                        },
                        {
                            "volume_id": "vol_logs",
                            "observed_status": "in-use",
                            "size_gb": 10.0,
                            "iops": 3000,
                            "throughput_mbps": 125,
                            "message": None,
                            "last_error": None,
                            "applied_version": 2,
                        },
                    ],
                    "stacks": [
                        {
                            "stack_id": "stack_abc123",
                            "observed_status": "running",
                            "message": None,
                            "last_error": None,
                            "containers": [
                                {
                                    "container_id": "ctr_a1b2c3",
                                    "observed_status": "running",
                                    "runtime_id": "sha256:abc123def456",
                                    "message": None,
                                    "last_error": None,
                                    "applied_version": 1,
                                },
                                {
                                    "container_id": "ctr_d4e5f6",
                                    "observed_status": "running",
                                    "runtime_id": "sha256:789ghi012jkl",
                                    "message": None,
                                    "last_error": None,
                                    "applied_version": 3,
                                },
                            ],
                            "applied_version": 1,
                        },
                        {
                            "stack_id": "stack_def456",
                            "observed_status": "error",
                            "message": "Worker container crashed",
                            "last_error": "Error: connect ECONNREFUSED 127.0.0.1:6379",
                            "containers": [
                                {
                                    "container_id": "ctr_g7h8i9",
                                    "observed_status": "error",
                                    "runtime_id": None,
                                    "message": "Container failed to start",
                                    "last_error": "Error: connect ECONNREFUSED 127.0.0.1:6379",
                                    "applied_version": 2,
                                },
                            ],
                            "applied_version": 4,
                        },
                    ],
                    "resources": {
                        "memory_gb": {"total": 16.0, "available": 12.5, "allocated": 3.5},
                        "cpu_cores": {"total": 8.0, "available": 6.0, "allocated": 2.0},
                        "disk_gb": {"total": 100.0, "available": 85.3, "allocated": 14.7},
                    },
                    "agent_version": "1.4.2",
                    "spec_revision": 42,
                    "reported_at_unix": 1736942400,
                }
            ]
        }
    )

    networks: list[AgentNetworkStatusReport] = []
    volumes: list[AgentVolumeStatusReport] = []
    stacks: list[AgentStackStatusReport] = []
    resources: AgentResourceReport = AgentResourceReport()
    agent_version: str | None = None
    spec_revision: int | None = Field(
        default=None,
        description="Revision of the node spec this report is based on",
        examples=[42],
    )
    reported_at_unix: int = Field(description="UTC timestamp in seconds since epoch")


ReportAgentNodeStatusResponse = EmptyResponse
