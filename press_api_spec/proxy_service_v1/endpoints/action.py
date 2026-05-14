from __future__ import annotations

from press_api_spec.proxy_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.proxy_service_v1.models.action import (
    GetActionResponse,
    ListActionsQuery,
    ListActionsResponse,
)

__all__ = [
    "actions",
    "ListActions",
    "GetAction",
]

actions = EndpointGroup(prefix="/actions", tags=("Actions",))

ListActions = actions.add(
    Endpoint(
        method=Method.GET,
        path="",
        query=ListActionsQuery,
        response=ListActionsResponse,
        name="list_actions",
        summary="List all action records across all resources",
    )
)

GetAction = actions.add(
    Endpoint(
        method=Method.GET,
        path="/<action_id>",
        response=GetActionResponse,
        name="get_action",
        summary="Fetch an action record by id",
    )
)
