"""Agent sync models — reconciliation between control plane and node agents.

Reconciliation is driven by observed state. The agent runs an idempotent reconcile
loop every cycle; convergence is reported per-resource via `observed_status`,
`reason`, `message`, and `blocked_on`.

reason
    Short machine-readable explanation of why the resource is in its current state.
    Examples: "waiting for dependency", "image pull failed", "address conflict".

message
    Human-readable free-text description suitable for display in a UI or log.

blocked_on
    Structured list of dependencies preventing forward progress. Each entry
    specifies the resource type, resource ID, and the condition being waited for.
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
    "PortMapSpec",
    "AgentDesiredStackSpec",
    "AgentNodeSpec",
    "GetAgentNodeSpecResponse",
    "Dependency",
    "AgentNetworkStatusReport",
    "AgentVolumeStatusReport",
    "AgentContainerStatusReport",
    "AgentStackStatusReport",
    "AgentResourceMetrics",
    "AgentResourceReport",
    "ReportAgentNodeStatusRequest",
    "ReportAgentNodeStatusResponse",
    "VolumeAgentNodeSpec",
    "GetVolumeAgentNodeSpecResponse",
    "VolumeAgentStatusReport",
    "ReportVolumeAgentStatusRequest",
    "ReportVolumeAgentStatusResponse",
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
                },
                {
                    "id": "net_def456",
                    "name": "staging-overlay",
                    "cidr": "10.1.0.0/16",
                    "gateway_ip": "10.1.0.1",
                },
            ]
        }
    )

    id: str = Field(description="Network ID assigned by the control plane")
    name: str = Field(examples=["production-overlay", "staging-overlay"])
    cidr: str = Field(examples=["10.0.0.0/16", "10.1.0.0/16"])
    gateway_ip: str = Field(examples=["10.0.0.1", "10.1.0.1"])


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
                },
                {
                    "id": "vol_logs",
                    "name": "app-logs",
                    "size_gb": 10.0,
                    "mountpoint": "/var/log/app",
                    "status": "available",
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


class PortMapSpec(BaseModel):
    node_port: int = Field(description="Port on the node (host)")
    container_port: int = Field(description="Port inside the container")


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
                        },
                    ],
                    "port_map": [
                        {
                            "node_port": 8080,
                            "container_port": 80,
                        }
                    ],
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
                        },
                    ],
                    "port_map": [],
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
    port_map: list[PortMapSpec] = []


class AgentNodeSpec(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "node_id": "node_us-east-1_001",
                    "networks": [
                        {
                            "id": "net_abc123",
                            "name": "production-overlay",
                            "cidr": "10.0.0.0/16",
                            "gateway_ip": "10.0.0.1",
                        },
                    ],
                    "volumes": [
                        {
                            "id": "vol_pgdata",
                            "name": "postgres-data",
                            "size_gb": 50.0,
                            "mountpoint": "/var/lib/postgresql/data",
                            "status": "in-use",
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
                                },
                            ],
                        },
                    ],
                }
            ]
        }
    )

    node_id: str = Field(description="Node this spec is scoped to")
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
                        "networks": [
                            {
                                "id": "net_abc123",
                                "name": "production-overlay",
                                "cidr": "10.0.0.0/16",
                                "gateway_ip": "10.0.0.1",
                            }
                        ],
                        "volumes": [
                            {
                                "id": "vol_pgdata",
                                "name": "postgres-data",
                                "size_gb": 50.0,
                                "mountpoint": "/var/lib/postgresql/data",
                                "status": "in-use",
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
                                    },
                                ],
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


class Dependency(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "resource_type": "volume",
                    "resource_id": "vol_pgdata",
                    "condition": "ready",
                },
                {
                    "resource_type": "container",
                    "resource_id": "ctr_redis",
                    "condition": "running",
                },
            ]
        }
    )

    resource_type: str = Field(
        description="Type of resource being waited on",
        examples=["volume", "network", "container"],
    )
    resource_id: str = Field(
        description="ID of the resource being waited on",
        examples=["vol_pgdata", "net_abc123", "ctr_redis"],
    )
    condition: str = Field(
        description="What condition the resource must satisfy",
        examples=["ready", "attached", "running"],
    )


class AgentNetworkStatusReport(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "network_id": "net_abc123",
                    "observed_status": "available",
                    "message": None,
                    "last_error": None,
                    "reason": None,
                    "blocked_on": [],
                },
                {
                    "network_id": "net_def456",
                    "observed_status": "error",
                    "message": "Failed to create overlay network",
                    "last_error": "address space already in use",
                    "reason": "address conflict",
                    "blocked_on": [],
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
    reason: str | None = Field(
        default=None,
        description="Why the resource is in this state, e.g. 'address conflict', 'waiting for upstream'",
    )
    blocked_on: list[Dependency] = []


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
                    "reason": None,
                    "blocked_on": [],
                },
                {
                    "volume_id": "vol_logs",
                    "observed_status": "error",
                    "size_gb": 10.0,
                    "iops": 3000,
                    "throughput_mbps": 125,
                    "message": "Volume mount failed",
                    "last_error": "device not found",
                    "reason": "device missing",
                    "blocked_on": [],
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
    reason: str | None = Field(
        default=None,
        description="Why the resource is in this state, e.g. 'provisioning', 'device missing'",
    )
    blocked_on: list[Dependency] = []


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
                    "reason": None,
                    "blocked_on": [],
                },
                {
                    "container_id": "ctr_d4e5f6",
                    "observed_status": "pending",
                    "runtime_id": None,
                    "message": "Waiting for volume to be ready before starting container",
                    "last_error": None,
                    "reason": "waiting for dependency",
                    "blocked_on": [
                        {
                            "resource_type": "volume",
                            "resource_id": "vol_pgdata",
                            "condition": "ready",
                        }
                    ],
                },
                {
                    "container_id": "ctr_dead",
                    "observed_status": "error",
                    "runtime_id": "sha256:789ghi012jkl",
                    "message": "Container exited with code 1",
                    "last_error": "FATAL: too many connections for role 'app'",
                    "reason": "application crash",
                    "blocked_on": [],
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
    reason: str | None = Field(
        default=None,
        description="Why the container is in this state, e.g. 'waiting for dependency', 'image pull failed'",
    )
    blocked_on: list[Dependency] = []


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
                            "reason": None,
                            "blocked_on": [],
                        },
                        {
                            "container_id": "ctr_d4e5f6",
                            "observed_status": "running",
                            "runtime_id": "sha256:789ghi012jkl",
                            "message": None,
                            "last_error": None,
                            "reason": None,
                            "blocked_on": [],
                        },
                    ],
                    "reason": None,
                    "blocked_on": [],
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
                            "reason": "dependency unavailable",
                            "blocked_on": [],
                        },
                    ],
                    "reason": "container failure",
                    "blocked_on": [],
                },
            ]
        }
    )

    stack_id: str
    observed_status: StackStatus
    message: str | None = None
    last_error: str | None = None
    containers: list[AgentContainerStatusReport] = []
    reason: str | None = Field(
        default=None,
        description="Why the stack is in this state, e.g. 'container failure', 'network not ready'",
    )
    blocked_on: list[Dependency] = []


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
                            "reason": None,
                            "blocked_on": [],
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
                            "reason": None,
                            "blocked_on": [],
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
                                    "reason": None,
                                    "blocked_on": [],
                                },
                            ],
                            "reason": None,
                            "blocked_on": [],
                        },
                    ],
                    "resources": {
                        "memory_gb": {"total": 16.0, "available": 12.5, "allocated": 3.5},
                        "cpu_cores": {"total": 8.0, "available": 6.0, "allocated": 2.0},
                        "disk_gb": {"total": 100.0, "available": 85.3, "allocated": 14.7},
                    },
                    "agent_version": "1.4.2",
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
    reported_at_unix: int = Field(description="UTC timestamp in seconds since epoch")


ReportAgentNodeStatusResponse = EmptyResponse


# ---------------------------------------------------------------------------
# Volume Agent — separated from runtime agent
# ---------------------------------------------------------------------------
# The volume agent manages volume lifecycle (create, resize, attach, detach,
# delete) independently. The runtime agent only creates local Docker volumes
# for container mounts and reports them in container props.


class VolumeAgentNodeSpec(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "node_id": "node_us-east-1_001",
                    "volumes": [
                        {
                            "id": "vol_pgdata",
                            "name": "postgres-data",
                            "size_gb": 50.0,
                            "status": "available",
                        },
                    ],
                }
            ]
        }
    )

    node_id: str = Field(description="Node this spec is scoped to")
    volumes: list[AgentVolumeSpec] = []


class GetVolumeAgentNodeSpecResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "spec": {
                        "node_id": "node_us-east-1_001",
                        "volumes": [
                            {
                                "id": "vol_pgdata",
                                "name": "postgres-data",
                                "size_gb": 50.0,
                                "status": "available",
                            }
                        ],
                    }
                }
            ]
        }
    )

    spec: VolumeAgentNodeSpec


class VolumeAgentStatusReport(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "volume_id": "vol_pgdata",
                    "observed_status": "available",
                    "size_gb": 50.0,
                    "message": None,
                    "last_error": None,
                    "reason": None,
                    "blocked_on": [],
                },
            ]
        }
    )

    volume_id: str
    observed_status: VolumeStatus = Field(description="Observed state of the volume on this node")
    size_gb: float | None = Field(default=None, examples=[10.0, 50.0, 100.0])
    message: str | None = None
    last_error: str | None = None
    reason: str | None = Field(
        default=None,
        description="Why the resource is in this state, e.g. 'provisioning', 'device missing'",
    )
    blocked_on: list[Dependency] = []


class ReportVolumeAgentStatusRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "volumes": [
                        {
                            "volume_id": "vol_pgdata",
                            "observed_status": "available",
                            "size_gb": 50.0,
                            "message": None,
                            "last_error": None,
                            "reason": None,
                            "blocked_on": [],
                        },
                    ],
                    "agent_version": "1.0.0",
                    "reported_at_unix": 1736942400,
                }
            ]
        }
    )

    volumes: list[VolumeAgentStatusReport] = []
    agent_version: str | None = None
    reported_at_unix: int = Field(description="UTC timestamp in seconds since epoch")


ReportVolumeAgentStatusResponse = EmptyResponse
