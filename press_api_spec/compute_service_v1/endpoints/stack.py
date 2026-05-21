from __future__ import annotations

from typing import TypeAlias

from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.compute_service_v1.models.activity import (
    ListActivityLogsQuery,
    ListActivityLogsResponse,
)
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
    "StackGroup",
    "CreateStack",
    "ListStacks",
    "GetStack",
    "UpdateStack",
    "DeleteStack",
    "ResizeStack",
    "StartStack",
    "StopStack",
    "RestartStack",
    "ListStackActivity",
]


StackGroup = EndpointGroup(prefix="/api/stacks", tags=("Stacks",))


class CreateStack(Endpoint):
    method = Method.POST
    path = ""
    name = "create_stack"
    summary = "Create a new compute stack"
    Body: TypeAlias = CreateStackRequest
    Response: TypeAlias = CreateStackResponse


StackGroup.add(CreateStack)


class ListStacks(Endpoint):
    method = Method.GET
    path = ""
    name = "list_stacks"
    summary = "Return a paginated list of stacks"
    Response: TypeAlias = ListStacksResponse
    Query: TypeAlias = ListStacksQuery


StackGroup.add(ListStacks)


class GetStack(Endpoint):
    method = Method.GET
    path = "/<stack_id>"
    name = "get_stack"
    summary = "Fetch a single stack by id"
    Response: TypeAlias = GetStackResponse


StackGroup.add(GetStack)


class UpdateStack(Endpoint):
    method = Method.PATCH
    path = "/<stack_id>"
    name = "update_stack"
    summary = "Update mutable stack attributes (description)"
    Body: TypeAlias = UpdateStackRequest
    Response: TypeAlias = UpdateStackResponse


StackGroup.add(UpdateStack)


class DeleteStack(Endpoint):
    method = Method.DELETE
    path = "/<stack_id>"
    name = "delete_stack"
    summary = "Delete a stack"
    Response: TypeAlias = DeleteStackResponse


StackGroup.add(DeleteStack)


class ResizeStack(Endpoint):
    method = Method.POST
    path = "/<stack_id>/actions/resize"
    name = "resize_stack"
    summary = "Resize a stack"
    Body: TypeAlias = ResizeStackRequest
    Response: TypeAlias = ResizeStackResponse


StackGroup.add(ResizeStack)


class StartStack(Endpoint):
    method = Method.POST
    path = "/<stack_id>/actions/start"
    name = "start_stack"
    summary = "Start a stopped stack"
    Response: TypeAlias = StackActionResponse


StackGroup.add(StartStack)


class StopStack(Endpoint):
    method = Method.POST
    path = "/<stack_id>/actions/stop"
    name = "stop_stack"
    summary = "Stop a running stack"
    Response: TypeAlias = StackActionResponse


StackGroup.add(StopStack)


class RestartStack(Endpoint):
    method = Method.POST
    path = "/<stack_id>/actions/restart"
    name = "restart_stack"
    summary = "Restart a stack"
    Response: TypeAlias = StackActionResponse


StackGroup.add(RestartStack)


class ListStackActivity(Endpoint):
    method = Method.GET
    path = "/<stack_id>/activity"
    name = "list_stack_activity"
    summary = "List activity log entries for a stack"
    Response: TypeAlias = ListActivityLogsResponse
    Query: TypeAlias = ListActivityLogsQuery


StackGroup.add(ListStackActivity)
