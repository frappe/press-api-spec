from __future__ import annotations

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
    "volumes",
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


volumes = EndpointGroup(prefix="/volumes", tags=("Volumes",))

CreateVolume = volumes.add(
    Endpoint(
        method=Method.POST,
        path="",
        body=CreateVolumeRequest,
        response=CreateVolumeResponse,
        name="create_volume",
        summary="Create a new block volume.",
    )
)

ListVolumes = volumes.add(
    Endpoint(
        method=Method.GET,
        path="",
        query=ListVolumesQuery,
        response=ListVolumesResponse,
        name="list_volumes",
        summary="Return a paginated list of volumes.",
    )
)

GetVolume = volumes.add(
    Endpoint(
        method=Method.GET,
        path="/<volume_id>",
        response=GetVolumeResponse,
        name="get_volume",
        summary="Fetch a single volume by id.",
    )
)

UpdateVolume = volumes.add(
    Endpoint(
        method=Method.PATCH,
        path="/<volume_id>",
        body=UpdateVolumeRequest,
        response=UpdateVolumeResponse,
        name="update_volume",
        summary="Update mutable volume attributes (description).",
    )
)

DeleteVolume = volumes.add(
    Endpoint(
        method=Method.DELETE,
        path="/<volume_id>",
        response=DeleteVolumeResponse,
        name="delete_volume",
        summary="Delete a volume.",
    )
)

AttachVolume = volumes.add(
    Endpoint(
        method=Method.POST,
        path="/<volume_id>/actions/attach",
        body=AttachVolumeRequest,
        response=AttachVolumeResponse,
        name="attach_volume",
        summary="Attach a volume to an instance.",
    )
)

DetachVolume = volumes.add(
    Endpoint(
        method=Method.POST,
        path="/<volume_id>/actions/detach",
        body=DetachVolumeRequest,
        response=DetachVolumeResponse,
        name="detach_volume",
        summary="Detach a volume from its instance.",
    )
)

ResizeVolume = volumes.add(
    Endpoint(
        method=Method.POST,
        path="/<volume_id>/actions/resize",
        body=ResizeVolumeRequest,
        response=ResizeVolumeResponse,
        name="resize_volume",
        summary="Resize a volume.",
    )
)

SnapshotVolume = volumes.add(
    Endpoint(
        method=Method.POST,
        path="/<volume_id>/actions/snapshot",
        body=SnapshotVolumeRequest,
        response=SnapshotVolumeResponse,
        name="snapshot_volume",
        summary="Create a snapshot of a volume.",
    )
)
