from __future__ import annotations

from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup, Method
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
    "containers",
    "CreateContainer",
    "ListContainers",
    "GetContainer",
    "UpdateContainer",
    "DeleteContainer",
    "ResizeContainer",
    "StartContainer",
    "StopContainer",
    "RestartContainer",
]


containers = EndpointGroup(
    prefix="/stacks/<stack_id>/containers",
    tags=("Containers",),
)

CreateContainer = containers.add(
    Endpoint(
        method=Method.POST,
        path="",
        body=CreateContainerRequest,
        response=CreateContainerResponse,
        name="create_container",
        summary="Create a container inside a stack",
    )
)

ListContainers = containers.add(
    Endpoint(
        method=Method.GET,
        path="",
        query=ListContainersQuery,
        response=ListContainersResponse,
        name="list_containers",
        summary="List containers in a stack",
    )
)

GetContainer = containers.add(
    Endpoint(
        method=Method.GET,
        path="/<container_id>",
        response=GetContainerResponse,
        name="get_container",
        summary="Fetch a single container by id",
    )
)

UpdateContainer = containers.add(
    Endpoint(
        method=Method.PATCH,
        path="/<container_id>",
        body=UpdateContainerRequest,
        response=UpdateContainerResponse,
        name="update_container",
        summary="Update mutable container attributes (image, command, env)",
    )
)

DeleteContainer = containers.add(
    Endpoint(
        method=Method.DELETE,
        path="/<container_id>",
        response=DeleteContainerResponse,
        name="delete_container",
        summary="Delete a container",
    )
)

ResizeContainer = containers.add(
    Endpoint(
        method=Method.POST,
        path="/<container_id>/actions/resize",
        body=ResizeContainerRequest,
        response=ResizeContainerResponse,
        name="resize_container",
        summary="Resize memory limits for a container",
    )
)

StartContainer = containers.add(
    Endpoint(
        method=Method.POST,
        path="/<container_id>/actions/start",
        response=ContainerActionResponse,
        name="start_container",
        summary="Start a stopped container",
    )
)

StopContainer = containers.add(
    Endpoint(
        method=Method.POST,
        path="/<container_id>/actions/stop",
        response=ContainerActionResponse,
        name="stop_container",
        summary="Stop a running container",
    )
)

RestartContainer = containers.add(
    Endpoint(
        method=Method.POST,
        path="/<container_id>/actions/restart",
        response=ContainerActionResponse,
        name="restart_container",
        summary="Restart a container",
    )
)
