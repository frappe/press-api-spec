from __future__ import annotations

from press_api_spec.proxy_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.proxy_service_v1.models.redirect import (
    CreateRedirectRequest,
    CreateRedirectResponse,
    DeleteRedirectResponse,
    GetRedirectResponse,
    ListRedirectsQuery,
    ListRedirectsResponse,
    UpdateRedirectRequest,
)

__all__ = [
    "redirects",
    "CreateRedirect",
    "ListRedirects",
    "GetRedirect",
    "UpdateRedirect",
    "DeleteRedirect",
]

redirects = EndpointGroup(prefix="/proxy/domains/<domain_id>/redirects", tags=("Redirects",))

CreateRedirect = redirects.add(
    Endpoint(
        method=Method.POST,
        path="",
        body=CreateRedirectRequest,
        response=CreateRedirectResponse,
        name="create_redirect",
        summary="Create a redirect rule for a domain",
    )
)

ListRedirects = redirects.add(
    Endpoint(
        method=Method.GET,
        path="",
        query=ListRedirectsQuery,
        response=ListRedirectsResponse,
        name="list_redirects",
        summary="List redirect rules for a domain",
    )
)

GetRedirect = redirects.add(
    Endpoint(
        method=Method.GET,
        path="/<redirect_id>",
        response=GetRedirectResponse,
        name="get_redirect",
        summary="Get a redirect rule",
    )
)

UpdateRedirect = redirects.add(
    Endpoint(
        method=Method.PATCH,
        path="/<redirect_id>",
        body=UpdateRedirectRequest,
        response=CreateRedirectResponse,
        name="update_redirect",
        summary="Update a redirect rule",
    )
)

DeleteRedirect = redirects.add(
    Endpoint(
        method=Method.DELETE,
        path="/<redirect_id>",
        response=DeleteRedirectResponse,
        name="delete_redirect",
        summary="Delete a redirect rule",
    )
)
