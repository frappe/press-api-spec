from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

from press_api_spec.compute_service_v1.base import EmptyResponse, Paginated, PaginationParams

__all__ = [
    "VolumeStatus",
    "VolumeMountStatus",
    "SnapshotStatus",
    "VolumeMount",
    "Volume",
    "Snapshot",
    "CreateVolumeRequest",
    "CreateVolumeResponse",
    "GetVolumeResponse",
    "ListVolumesQuery",
    "ListVolumesResponse",
    "UpdateVolumeRequest",
    "UpdateVolumeResponse",
    "DeleteVolumeResponse",
    "AttachVolumeRequest",
    "AttachVolumeResponse",
    "DetachVolumeRequest",
    "DetachVolumeResponse",
    "ResizeVolumeRequest",
    "ResizeVolumeResponse",
    "SnapshotVolumeRequest",
    "SnapshotVolumeResponse",
    "GetSnapshotResponse",
    "ListSnapshotsQuery",
    "ListSnapshotsResponse",
    "DeleteSnapshotResponse",
]


class VolumeStatus(str, Enum):
    CREATING = "creating"
    AVAILABLE = "available"
    ATTACHING = "attaching"
    IN_USE = "in-use"
    DETACHING = "detaching"
    DELETING = "deleting"
    DELETED = "deleted"
    ERROR = "error"


class VolumeMountStatus(str, Enum):
    ATTACHING = "attaching"
    DETACHING = "detaching"
    MODIFYING = "modifying"
    DELETING = "deleting"
    ATTACHED = "attached"


class SnapshotStatus(str, Enum):
    PENDING = "pending"
    CREATING = "creating"
    AVAILABLE = "available"
    DELETING = "deleting"
    ERROR = "error"


class VolumeMount(BaseModel):
    stack_id: str
    container_id: str
    mountpoint: str = Field(examples=["/data", "/var/lib/postgresql"])
    status: VolumeMountStatus = VolumeMountStatus.ATTACHED


class Volume(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "vol_abc123",
                    "description": "PostgreSQL data",
                    "size": 100,
                    "status": "in-use",
                    "mounts": [
                        {
                            "stack_id": "stack_abc123",
                            "container_id": "ctr_def456",
                            "mountpoint": "/var/lib/postgresql",
                            "status": "attached",
                        }
                    ],
                    "created_at_unix": 1736935200,
                    "updated_at_unix": 1736942400,
                },
                {
                    "id": "vol_def456",
                    "description": "Redis cache",
                    "size": 20,
                    "status": "available",
                    "mounts": [],
                    "created_at_unix": 1736949600,
                    "updated_at_unix": 1736956800,
                },
            ]
        }
    )

    id: str
    name: str = Field(examples=["postgres-data", "app-logs"])
    description: str = Field(examples=["PostgreSQL data", "Redis cache"])
    size: int = Field(examples=[10, 100, 500])
    status: VolumeStatus = VolumeStatus.CREATING
    mounts: list[VolumeMount] = []
    created_at_unix: int
    updated_at_unix: int


class Snapshot(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "snap_abc123",
                    "description": "Pre-deployment backup",
                    "volume_id": "vol_abc123",
                    "size": 100,
                    "status": "available",
                    "created_at_unix": 1736935200,
                    "updated_at_unix": 1736935500,
                }
            ]
        }
    )

    id: str
    description: str
    volume_id: str
    size: int
    status: SnapshotStatus = SnapshotStatus.PENDING
    created_at_unix: int
    updated_at_unix: int


class CreateVolumeRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "description": "PostgreSQL data",
                    "size": 100,
                    "snapshot_id": None,
                }
            ]
        }
    )

    name: str = Field(examples=["postgres-data", "app-logs"])
    description: str = Field(examples=["PostgreSQL data", "Redis cache"])
    size: int = Field(examples=[10, 100, 500])
    snapshot_id: str | None = None


class CreateVolumeResponse(BaseModel):
    volume: Volume


class ListVolumesQuery(PaginationParams):
    status: VolumeStatus | None = None
    stack_id: str | None = Field(default=None, examples=["stack_abc123"])


ListVolumesResponse = Paginated[Volume]


class GetVolumeResponse(BaseModel):
    volume: Volume


class UpdateVolumeRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"examples": [{"description": "Renamed: PostgreSQL primary"}]}
    )

    description: str | None = Field(default=None, examples=["Renamed: PostgreSQL primary"])


class UpdateVolumeResponse(BaseModel):
    volume: Volume


DeleteVolumeResponse = EmptyResponse


class AttachVolumeRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "stack_id": "stack_abc123",
                    "container_id": "ctr_def456",
                    "mountpoint": "/var/lib/postgresql",
                }
            ]
        }
    )

    stack_id: str
    container_id: str
    mountpoint: str = Field(examples=["/data", "/var/lib/postgresql"])


class AttachVolumeResponse(BaseModel):
    volume: Volume


class DetachVolumeRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={"examples": [{"container_id": "ctr_def456"}]})

    container_id: str


class DetachVolumeResponse(BaseModel):
    volume: Volume


class ResizeVolumeRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"examples": [{"size": 200, "iops": 6000, "throughput": 250}]}
    )

    size: int | None = None
    iops: int | None = None
    throughput: int | None = None


class ResizeVolumeResponse(BaseModel):
    volume: Volume


class SnapshotVolumeRequest(BaseModel):
    description: str = Field(examples=["Pre-deployment backup", "Weekly snapshot"])


class SnapshotVolumeResponse(BaseModel):
    snapshot: Snapshot


class GetSnapshotResponse(BaseModel):
    snapshot: Snapshot


class ListSnapshotsQuery(PaginationParams):
    volume_id: str | None = Field(default=None, examples=["vol_abc123"])
    status: SnapshotStatus | None = None


ListSnapshotsResponse = Paginated[Snapshot]


DeleteSnapshotResponse = EmptyResponse
