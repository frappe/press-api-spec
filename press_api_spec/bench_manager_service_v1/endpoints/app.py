from __future__ import annotations

from typing import TypeAlias

from press_api_spec.bench_manager_service_v1.models import (
    AddAppRequest,
    AddAppResponse,
    HealthResponse,
    RemoveAppRequest,
    RemoveAppResponse,
)
from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup, Method

__all__ = [
    "AppGroup",
    "AddApp",
    "RemoveApp",
    "Health",
]


AppGroup = EndpointGroup(
    prefix="/apps",
    tags=("Apps",),
)

class AddApp(Endpoint):
    method = Method.POST
    path = "/add-app"
    name = "add_app"
    summary = "Add an app to the bench, reusing an existing AppSource if present"
    Body: TypeAlias = AddAppRequest
    Response: TypeAlias = AddAppResponse

AppGroup.add(AddApp)

class RemoveApp(Endpoint):
    method = Method.POST
    path = "/remove-app"
    name = "remove_app"
    summary = "Remove an app from the bench, preserving AppSource and AppRelease history"
    Body: TypeAlias = RemoveAppRequest
    Response: TypeAlias = RemoveAppResponse

AppGroup.add(RemoveApp)

class Health(Endpoint):
    method = Method.GET
    path = "/health"
    name = "health"
    summary = "Sanity check for the bench manager app service"
    Response: TypeAlias = HealthResponse

AppGroup.add(Health)
