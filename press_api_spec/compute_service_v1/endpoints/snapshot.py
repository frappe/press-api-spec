from __future__ import annotations

from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.compute_service_v1.models.volume import (
    DeleteSnapshotResponse,
    GetSnapshotResponse,
    ListSnapshotsQuery,
    ListSnapshotsResponse,
)

__all__ = [
    "snapshots",
    "ListSnapshots",
    "GetSnapshot",
    "DeleteSnapshot",
]


snapshots = EndpointGroup(prefix="/snapshots", tags=("Snapshots",))

ListSnapshots = snapshots.add(
    Endpoint(
        method=Method.GET,
        path="",
        query=ListSnapshotsQuery,
        response=ListSnapshotsResponse,
        name="list_snapshots",
        summary="Return a paginated list of snapshots.",
    )
)

GetSnapshot = snapshots.add(
    Endpoint(
        method=Method.GET,
        path="/<snapshot_id>",
        response=GetSnapshotResponse,
        name="get_snapshot",
        summary="Fetch a single snapshot by id.",
    )
)

DeleteSnapshot = snapshots.add(
    Endpoint(
        method=Method.DELETE,
        path="/<snapshot_id>",
        response=DeleteSnapshotResponse,
        name="delete_snapshot",
        summary="Delete a snapshot.",
    )
)
