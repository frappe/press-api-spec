from __future__ import annotations

from press_api_spec.bench_manager_service_v1.models import (
    AddAppRequest,
    AddAppResponse,
    HealthResponse,
    RemoveAppRequest,
    RemoveAppResponse,
)
from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup, Method

__all__ = [
    "apps",
    "AddApp",
    "RemoveApp",
    "Health",
]


apps = EndpointGroup(
    prefix="/apps",
    tags=("Apps",),
)

AddApp = apps.add(
    Endpoint(
        method=Method.POST,
        path="/add-app",
        body=AddAppRequest,
        response=AddAppResponse,
        name="add_app",
        summary="Add an app to the bench, reusing an existing AppSource if present",
    )
)

RemoveApp = apps.add(
    Endpoint(
        method=Method.POST,
        path="/remove-app",
        body=RemoveAppRequest,
        response=RemoveAppResponse,
        name="remove_app",
        summary="Remove an app from the bench, preserving AppSource and AppRelease history",
    )
)

Health = apps.add(
    Endpoint(
        method=Method.GET,
        path="/health",
        response=HealthResponse,
        name="health",
        summary="Sanity check for the bench manager app service",
    )
)
