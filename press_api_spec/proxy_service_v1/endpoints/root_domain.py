from __future__ import annotations

from typing import TypeAlias

from press_api_spec.proxy_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.proxy_service_v1.models.root_domain import (
    ConfigureRootDomainRequest,
    ConfigureRootDomainResponse,
    ListRootDomainsQuery,
    ListRootDomainsResponse,
    GetRootDomainResponse,
    DeleteRootDomainResponse,
)

__all__ = [
    "RootDomainGroup",
    "CreateRootDomain",
    "ListRootDomains",
    "GetRootDomain",
    "UpdateRootDomain",
    "DeleteRootDomain",
]

RootDomainGroup = EndpointGroup(prefix="/api/proxy/root-domains", tags=("Root Domains",))


class CreateRootDomain(Endpoint):
    method = Method.POST
    path = ""
    name = "create_root_domain"
    summary = "Configure a new root domain"
    Body: TypeAlias = ConfigureRootDomainRequest
    Response: TypeAlias = ConfigureRootDomainResponse


RootDomainGroup.add(CreateRootDomain)


class ListRootDomains(Endpoint):
    method = Method.GET
    path = ""
    name = "list_root_domains"
    summary = "List all configured root domains"
    Response: TypeAlias = ListRootDomainsResponse
    Query: TypeAlias = ListRootDomainsQuery


RootDomainGroup.add(ListRootDomains)


class GetRootDomain(Endpoint):
    method = Method.GET
    path = "/<root_domain_id>"
    name = "get_root_domain"
    summary = "Get root domain details"
    Response: TypeAlias = GetRootDomainResponse


RootDomainGroup.add(GetRootDomain)


class UpdateRootDomain(Endpoint):
    method = Method.PATCH
    path = "/<root_domain_id>"
    name = "update_root_domain"
    summary = "Update an existing root domain configuration"
    Body: TypeAlias = ConfigureRootDomainRequest
    Response: TypeAlias = ConfigureRootDomainResponse


RootDomainGroup.add(UpdateRootDomain)


class DeleteRootDomain(Endpoint):
    method = Method.DELETE
    path = "/<root_domain_id>"
    name = "delete_root_domain"
    summary = "Delete a root domain configuration"
    Response: TypeAlias = DeleteRootDomainResponse


RootDomainGroup.add(DeleteRootDomain)
