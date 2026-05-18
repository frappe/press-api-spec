from __future__ import annotations

from typing import TypeAlias

from press_api_spec.proxy_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.proxy_service_v1.models.action import (
    GetActionResponse,
    ListActionsQuery,
    ListActionsResponse,
)
from press_api_spec.proxy_service_v1.models.domain import (
    DeleteDomainResponse,
    GetCertificateChainResponse,
    GetDomainResponse,
    ListDomainsQuery,
    ListDomainsResponse,
    RegisterDomainRequest,
    RegisterDomainResponse,
    RenewCertificateResponse,
    VerifyDomainResponse,
)

__all__ = [
    "DomainGroup",
    "RegisterDomain",
    "ListDomains",
    "GetDomain",
    "VerifyDomain",
    "GetCertificateChain",
    "RenewCertificate",
    "DeleteDomain",
    "ListDomainActions",
    "GetDomainAction",
]

DomainGroup = EndpointGroup(prefix="/api/proxy/domains", tags=("Domains",))

class RegisterDomain(Endpoint):
    method = Method.POST
    path = ""
    name = "register_domain"
    summary = "Register a domain for proxy routing"
    Body: TypeAlias = RegisterDomainRequest
    Response: TypeAlias = RegisterDomainResponse

DomainGroup.add(RegisterDomain)

class ListDomains(Endpoint):
    method = Method.GET
    path = ""
    name = "list_domains"
    summary = "List registered domains"
    Response: TypeAlias = ListDomainsResponse
    Query: TypeAlias = ListDomainsQuery

DomainGroup.add(ListDomains)

class GetDomain(Endpoint):
    method = Method.GET
    path = "/<domain_id>"
    name = "get_domain"
    summary = "Get domain details including DNS records and TLS certificate info"
    Response: TypeAlias = GetDomainResponse

DomainGroup.add(GetDomain)

class VerifyDomain(Endpoint):
    method = Method.POST
    path = "/<domain_id>/actions/verify"
    name = "verify_domain"
    summary = "Trigger DNS verification for a domain"
    Response: TypeAlias = VerifyDomainResponse

DomainGroup.add(VerifyDomain)

class GetCertificateChain(Endpoint):
    method = Method.GET
    path = "/<domain_id>/certificate"
    name = "get_certificate_chain"
    summary = "Fetch the full TLS certificate chain (PEM) for a domain"
    Response: TypeAlias = GetCertificateChainResponse

DomainGroup.add(GetCertificateChain)

class RenewCertificate(Endpoint):
    method = Method.POST
    path = "/<domain_id>/actions/renew-certificate"
    name = "renew_certificate"
    summary = "Force renewal of the TLS certificate for a domain"
    Response: TypeAlias = RenewCertificateResponse

DomainGroup.add(RenewCertificate)

class DeleteDomain(Endpoint):
    method = Method.DELETE
    path = "/<domain_id>"
    name = "delete_domain"
    summary = "Unregister a domain"
    Response: TypeAlias = DeleteDomainResponse

DomainGroup.add(DeleteDomain)


class ListDomainActions(Endpoint):
    method = Method.GET
    path = "/actions"
    name = "list_domain_actions"
    summary = "List all action records for domains"
    Response: TypeAlias = ListActionsResponse
    Query: TypeAlias = ListActionsQuery

DomainGroup.add(ListDomainActions)


class GetDomainAction(Endpoint):
    method = Method.GET
    path = "/actions/<action_id>"
    name = "get_domain_action"
    summary = "Fetch a domain action record by id"
    Response: TypeAlias = GetActionResponse

DomainGroup.add(GetDomainAction)
