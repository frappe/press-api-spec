from __future__ import annotations

from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.compute_service_v1.models.stack import (
    CreateStackRequest,
    CreateStackResponse,
    DeleteStackResponse,
    GetStackResponse,
    StackActionResponse,
    ListStacksQuery,
    ListStacksResponse,
    ResizeStackRequest,
    ResizeStackResponse,
    UpdateStackRequest,
    UpdateStackResponse,
)

__all__ = [
    "stacks",
    "CreateStack",
    "ListStacks",
    "GetStack",
    "UpdateStack",
    "DeleteStack",
    "ResizeStack",
    "StartStack",
    "StopStack",
    "RestartStack",
]


stacks = EndpointGroup(prefix="/stacks", tags=("Stacks",))

CreateStack = stacks.add(
    Endpoint(
        method=Method.POST,
        path="",
        body=CreateStackRequest,
        response=CreateStackResponse,
        name="create_stack",
        summary="Create a new compute stack",
    )
)

ListStacks = stacks.add(
    Endpoint(
        method=Method.GET,
        path="",
        query=ListStacksQuery,
        response=ListStacksResponse,
        name="list_stacks",
        summary="Return a paginated list of stacks",
    )
)

GetStack = stacks.add(
    Endpoint(
        method=Method.GET,
        path="/<stack_id>",
        response=GetStackResponse,
        name="get_stack",
        summary="Fetch a single stack by id",
    )
)

UpdateStack = stacks.add(
    Endpoint(
        method=Method.PATCH,
        path="/<stack_id>",
        body=UpdateStackRequest,
        response=UpdateStackResponse,
        name="update_stack",
        summary="Update mutable stack attributes (name, description)",
    )
)

DeleteStack = stacks.add(
    Endpoint(
        method=Method.DELETE,
        path="/<stack_id>",
        response=DeleteStackResponse,
        name="delete_stack",
        summary="Delete a stack",
    )
)

ResizeStack = stacks.add(
    Endpoint(
        method=Method.POST,
        path="/<stack_id>/actions/resize",
        body=ResizeStackRequest,
        response=ResizeStackResponse,
        name="resize_stack",
        summary="Resize a stack",
    )
)

StartStack = stacks.add(
    Endpoint(
        method=Method.POST,
        path="/<stack_id>/actions/start",
        response=StackActionResponse,
        name="start_stack",
        summary="Start a stopped stack",
    )
)

StopStack = stacks.add(
    Endpoint(
        method=Method.POST,
        path="/<stack_id>/actions/stop",
        response=StackActionResponse,
        name="stop_stack",
        summary="Stop a running stack",
    )
)

RestartStack = stacks.add(
    Endpoint(
        method=Method.POST,
        path="/<stack_id>/actions/restart",
        response=StackActionResponse,
        name="restart_stack",
        summary="Restart a stack",
    )
)
