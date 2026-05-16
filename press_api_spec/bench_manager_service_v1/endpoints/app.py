from __future__ import annotations

from typing import TypeAlias

from press_api_spec.bench_manager_service_v1.models import (
    AddAppRequest,
    AddAppResponse,
    AppWebhookRequest,
    AppWebhookResponse,
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
    "AppWebhook",
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


class AppWebhook(Endpoint):
    method = Method.POST
    path = "/webhook"
    name = "app_webhook"
    summary = "Endpoint to receive webhook events for apps and trigger corresponding actions"
    Body: TypeAlias = AppWebhookRequest
    Response: TypeAlias = AppWebhookResponse


AppGroup.add(AppWebhook)
