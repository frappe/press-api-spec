from __future__ import annotations

from typing import TypeAlias

from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.compute_service_v1.models.volume import (
    AttachVolumeRequest,
    AttachVolumeResponse,
    CreateVolumeRequest,
    CreateVolumeResponse,
    DeleteVolumeResponse,
    DetachVolumeRequest,
    DetachVolumeResponse,
    GetVolumeResponse,
    ListVolumesQuery,
    ListVolumesResponse,
    ResizeVolumeRequest,
    ResizeVolumeResponse,
    SnapshotVolumeRequest,
    SnapshotVolumeResponse,
    UpdateVolumeRequest,
    UpdateVolumeResponse,
)

__all__ = [
    "VolumeGroup",
    "CreateVolume",
    "ListVolumes",
    "GetVolume",
    "UpdateVolume",
    "DeleteVolume",
    "AttachVolume",
    "DetachVolume",
    "ResizeVolume",
    "SnapshotVolume",
]


VolumeGroup = EndpointGroup(prefix="/api/volumes", tags=("Volumes",))

class CreateVolume(Endpoint):
    method = Method.POST
    path = ""
    name = "create_volume"
    summary = "Create a new block volume."
    Body: TypeAlias = CreateVolumeRequest
    Response: TypeAlias = CreateVolumeResponse

VolumeGroup.add(CreateVolume)

class ListVolumes(Endpoint):
    method = Method.GET
    path = ""
    name = "list_volumes"
    summary = "Return a paginated list of volumes."
    Response: TypeAlias = ListVolumesResponse
    Query: TypeAlias = ListVolumesQuery

VolumeGroup.add(ListVolumes)

class GetVolume(Endpoint):
    method = Method.GET
    path = "/<volume_id>"
    name = "get_volume"
    summary = "Fetch a single volume by id."
    Response: TypeAlias = GetVolumeResponse

VolumeGroup.add(GetVolume)

class UpdateVolume(Endpoint):
    method = Method.PATCH
    path = "/<volume_id>"
    name = "update_volume"
    summary = "Update mutable volume attributes (description)."
    Body: TypeAlias = UpdateVolumeRequest
    Response: TypeAlias = UpdateVolumeResponse

VolumeGroup.add(UpdateVolume)

class DeleteVolume(Endpoint):
    method = Method.DELETE
    path = "/<volume_id>"
    name = "delete_volume"
    summary = "Delete a volume."
    Response: TypeAlias = DeleteVolumeResponse

VolumeGroup.add(DeleteVolume)

class AttachVolume(Endpoint):
    method = Method.POST
    path = "/<volume_id>/actions/attach"
    name = "attach_volume"
    summary = "Attach a volume to an instance."
    Body: TypeAlias = AttachVolumeRequest
    Response: TypeAlias = AttachVolumeResponse

VolumeGroup.add(AttachVolume)

class DetachVolume(Endpoint):
    method = Method.POST
    path = "/<volume_id>/actions/detach"
    name = "detach_volume"
    summary = "Detach a volume from its instance."
    Body: TypeAlias = DetachVolumeRequest
    Response: TypeAlias = DetachVolumeResponse

VolumeGroup.add(DetachVolume)

class ResizeVolume(Endpoint):
    method = Method.POST
    path = "/<volume_id>/actions/resize"
    name = "resize_volume"
    summary = "Resize a volume."
    Body: TypeAlias = ResizeVolumeRequest
    Response: TypeAlias = ResizeVolumeResponse

VolumeGroup.add(ResizeVolume)

class SnapshotVolume(Endpoint):
    method = Method.POST
    path = "/<volume_id>/actions/snapshot"
    name = "snapshot_volume"
    summary = "Create a snapshot of a volume."
    Body: TypeAlias = SnapshotVolumeRequest
    Response: TypeAlias = SnapshotVolumeResponse

VolumeGroup.add(SnapshotVolume)
