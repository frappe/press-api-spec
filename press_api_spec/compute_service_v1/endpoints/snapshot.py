from __future__ import annotations

from typing import TypeAlias

from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.compute_service_v1.models.volume import (
    DeleteSnapshotResponse,
    GetSnapshotResponse,
    ListSnapshotsQuery,
    ListSnapshotsResponse,
)

__all__ = [
    "SnapshotGroup",
    "ListSnapshots",
    "GetSnapshot",
    "DeleteSnapshot",
]


SnapshotGroup = EndpointGroup(prefix="/snapshots", tags=("Snapshots",))

class ListSnapshots(Endpoint):
    method = Method.GET
    path = ""
    name = "list_snapshots"
    summary = "Return a paginated list of snapshots."
    Response: TypeAlias = ListSnapshotsResponse
    Query: TypeAlias = ListSnapshotsQuery

SnapshotGroup.add(ListSnapshots)

class GetSnapshot(Endpoint):
    method = Method.GET
    path = "/<snapshot_id>"
    name = "get_snapshot"
    summary = "Fetch a single snapshot by id."
    Response: TypeAlias = GetSnapshotResponse

SnapshotGroup.add(GetSnapshot)

class DeleteSnapshot(Endpoint):
    method = Method.DELETE
    path = "/<snapshot_id>"
    name = "delete_snapshot"
    summary = "Delete a snapshot."
    Response: TypeAlias = DeleteSnapshotResponse

SnapshotGroup.add(DeleteSnapshot)
