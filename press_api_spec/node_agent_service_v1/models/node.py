from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

__all__ = [
    "NodeStatus",
    "NodeInfo",
    "GetNodeInfoResponse",
    "UpdateNodeStatusRequest",
    "UpdateNodeStatusResponse",
]


class NodeStatus(str, Enum):
    READY = "ready"
    DRAINING = "draining"
    OFFLINE = "offline"
    ERROR = "error"


class NodeInfo(BaseModel):
    agent_id: str = Field(description="Unique identifier for this agent instance")
    node_id: str = Field(description="Unique identifier for this node")
    status: NodeStatus = NodeStatus.READY
    hostname: str | None = None
    ip_address: str | None = None
    total_memory_gb: float | None = None
    available_memory_gb: float | None = None
    total_cpu_cores: float | None = None
    available_cpu_cores: float | None = None
    disk_total_gb: float | None = None
    disk_available_gb: float | None = None
    runtime_version: str | None = Field(
        default=None, description="Container runtime version (e.g. docker 27.3.1)"
    )
    agent_version: str | None = None
    labels: dict[str, str] = Field(default_factory=dict)
    updated_at_unix: int = Field(
        description="UTC timestamp in seconds since epoch", examples=[1736942400]
    )


class GetNodeInfoResponse(BaseModel):
    node: NodeInfo


class UpdateNodeStatusRequest(BaseModel):
    status: NodeStatus


class UpdateNodeStatusResponse(BaseModel):
    node: NodeInfo
