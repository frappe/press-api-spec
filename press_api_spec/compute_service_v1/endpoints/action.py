from __future__ import annotations

from typing import TypeAlias

from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.compute_service_v1.models.action import (
    GetActionResponse,
    ListActionsQuery,
    ListActionsResponse,
)

__all__ = [
    "ActionGroup",
    "ListActions",
    "GetAction",
]

ActionGroup = EndpointGroup(prefix="/api/actions", tags=("Actions",))

class ListActions(Endpoint):
    method = Method.GET
    path = ""
    name = "list_actions"
    summary = "List all action records across all resources"
    Response: TypeAlias = ListActionsResponse
    Query: TypeAlias = ListActionsQuery

ActionGroup.add(ListActions)

class GetAction(Endpoint):
    method = Method.GET
    path = "/<action_id>"
    name = "get_action"
    summary = "Fetch an action record by id"
    Response: TypeAlias = GetActionResponse

ActionGroup.add(GetAction)
