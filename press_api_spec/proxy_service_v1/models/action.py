from __future__ import annotations

from pydantic import BaseModel

from press_api_spec.proxy_service_v1.base import (
    ActionName,
    ActionRecord,
    ActionStatus,
    Paginated,
    PaginationParams,
    ResourceType,
)

__all__ = [
    "ActionStatus",
    "ActionName",
    "ResourceType",
    "ActionRecord",
    "ListActionsQuery",
    "ListActionsResponse",
    "GetActionResponse",
]


class ListActionsQuery(PaginationParams):
    status: ActionStatus | None = None
    name: ActionName | None = None
    resource_type: ResourceType | None = None
    resource_id: str | None = None


ListActionsResponse = Paginated[ActionRecord]


class GetActionResponse(BaseModel):
    action: ActionRecord
