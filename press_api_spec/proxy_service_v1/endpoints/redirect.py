from __future__ import annotations

from typing import TypeAlias

from press_api_spec.proxy_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.proxy_service_v1.models.redirect import (
    CreateRedirectRequest,
    CreateRedirectResponse,
    DeleteRedirectResponse,
    GetRedirectResponse,
    ListRedirectsQuery,
    ListRedirectsResponse,
    UpdateRedirectRequest,
    UpdateRedirectResponse,
)

__all__ = [
    "RedirectGroup",
    "CreateRedirect",
    "ListRedirects",
    "GetRedirect",
    "UpdateRedirect",
    "DeleteRedirect",
]

RedirectGroup = EndpointGroup(
    prefix="/api/proxy/domains/<domain_id>/redirects", tags=("Redirects",)
)


class CreateRedirect(Endpoint):
    method = Method.POST
    path = ""
    name = "create_redirect"
    summary = "Create a redirect rule for a domain"
    Body: TypeAlias = CreateRedirectRequest
    Response: TypeAlias = CreateRedirectResponse


RedirectGroup.add(CreateRedirect)


class ListRedirects(Endpoint):
    method = Method.GET
    path = ""
    name = "list_redirects"
    summary = "List redirect rules for a domain"
    Response: TypeAlias = ListRedirectsResponse
    Query: TypeAlias = ListRedirectsQuery


RedirectGroup.add(ListRedirects)


class GetRedirect(Endpoint):
    method = Method.GET
    path = "/<redirect_id>"
    name = "get_redirect"
    summary = "Get a redirect rule"
    Response: TypeAlias = GetRedirectResponse


RedirectGroup.add(GetRedirect)


class UpdateRedirect(Endpoint):
    method = Method.PATCH
    path = "/<redirect_id>"
    name = "update_redirect"
    summary = "Update a redirect rule"
    Body: TypeAlias = UpdateRedirectRequest
    Response: TypeAlias = UpdateRedirectResponse


RedirectGroup.add(UpdateRedirect)


class DeleteRedirect(Endpoint):
    method = Method.DELETE
    path = "/<redirect_id>"
    name = "delete_redirect"
    summary = "Delete a redirect rule"
    Response: TypeAlias = DeleteRedirectResponse


RedirectGroup.add(DeleteRedirect)
