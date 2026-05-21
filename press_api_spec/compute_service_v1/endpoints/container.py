from __future__ import annotations

from typing import TypeAlias

from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.compute_service_v1.models.activity import (
    ListActivityLogsQuery,
    ListActivityLogsResponse,
)
from press_api_spec.compute_service_v1.models.container import (
    ContainerActionResponse,
    CreateContainerRequest,
    CreateContainerResponse,
    DeleteContainerResponse,
    GetContainerResponse,
    ListContainersQuery,
    ListContainersResponse,
    ResizeContainerRequest,
    ResizeContainerResponse,
    UpdateContainerRequest,
    UpdateContainerResponse,
)

__all__ = [
    "ContainerGroup",
    "CreateContainer",
    "ListContainers",
    "GetContainer",
    "UpdateContainer",
    "DeleteContainer",
    "ResizeContainer",
    "StartContainer",
    "StopContainer",
    "RestartContainer",
    "ListContainerActivity",
]


ContainerGroup = EndpointGroup(
    prefix="/api/stacks/<stack_id>/containers",
    tags=("Containers",),
)


class CreateContainer(Endpoint):
    method = Method.POST
    path = ""
    name = "create_container"
    summary = "Create a container inside a stack"
    Body: TypeAlias = CreateContainerRequest
    Response: TypeAlias = CreateContainerResponse


ContainerGroup.add(CreateContainer)


class ListContainers(Endpoint):
    method = Method.GET
    path = ""
    name = "list_containers"
    summary = "List containers in a stack"
    Response: TypeAlias = ListContainersResponse
    Query: TypeAlias = ListContainersQuery


ContainerGroup.add(ListContainers)


class GetContainer(Endpoint):
    method = Method.GET
    path = "/<container_id>"
    name = "get_container"
    summary = "Fetch a single container by id"
    Response: TypeAlias = GetContainerResponse


ContainerGroup.add(GetContainer)


class UpdateContainer(Endpoint):
    method = Method.PATCH
    path = "/<container_id>"
    name = "update_container"
    summary = "Update mutable container attributes (image, command, env)"
    Body: TypeAlias = UpdateContainerRequest
    Response: TypeAlias = UpdateContainerResponse


ContainerGroup.add(UpdateContainer)


class DeleteContainer(Endpoint):
    method = Method.DELETE
    path = "/<container_id>"
    name = "delete_container"
    summary = "Delete a container"
    Response: TypeAlias = DeleteContainerResponse


ContainerGroup.add(DeleteContainer)


class ResizeContainer(Endpoint):
    method = Method.POST
    path = "/<container_id>/actions/resize"
    name = "resize_container"
    summary = "Resize memory limits for a container"
    Body: TypeAlias = ResizeContainerRequest
    Response: TypeAlias = ResizeContainerResponse


ContainerGroup.add(ResizeContainer)


class StartContainer(Endpoint):
    method = Method.POST
    path = "/<container_id>/actions/start"
    name = "start_container"
    summary = "Start a stopped container"
    Response: TypeAlias = ContainerActionResponse


ContainerGroup.add(StartContainer)


class StopContainer(Endpoint):
    method = Method.POST
    path = "/<container_id>/actions/stop"
    name = "stop_container"
    summary = "Stop a running container"
    Response: TypeAlias = ContainerActionResponse


ContainerGroup.add(StopContainer)


class RestartContainer(Endpoint):
    method = Method.POST
    path = "/<container_id>/actions/restart"
    name = "restart_container"
    summary = "Restart a container"
    Response: TypeAlias = ContainerActionResponse


ContainerGroup.add(RestartContainer)


class ListContainerActivity(Endpoint):
    method = Method.GET
    path = "/<container_id>/activity"
    name = "list_container_activity"
    summary = "List activity log entries for a container"
    Response: TypeAlias = ListActivityLogsResponse
    Query: TypeAlias = ListActivityLogsQuery


ContainerGroup.add(ListContainerActivity)
