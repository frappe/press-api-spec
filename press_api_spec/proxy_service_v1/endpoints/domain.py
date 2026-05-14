from __future__ import annotations

from press_api_spec.proxy_service_v1.base import Endpoint, EndpointGroup, Method
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
    "domains",
    "RegisterDomain",
    "ListDomains",
    "GetDomain",
    "VerifyDomain",
    "GetCertificateChain",
    "RenewCertificate",
    "DeleteDomain",
]

domains = EndpointGroup(prefix="/proxy/domains", tags=("Domains",))

RegisterDomain = domains.add(
    Endpoint(
        method=Method.POST,
        path="",
        body=RegisterDomainRequest,
        response=RegisterDomainResponse,
        name="register_domain",
        summary="Register a domain for proxy routing",
    )
)

ListDomains = domains.add(
    Endpoint(
        method=Method.GET,
        path="",
        query=ListDomainsQuery,
        response=ListDomainsResponse,
        name="list_domains",
        summary="List registered domains",
    )
)

GetDomain = domains.add(
    Endpoint(
        method=Method.GET,
        path="/<domain_id>",
        response=GetDomainResponse,
        name="get_domain",
        summary="Get domain details including DNS records and TLS certificate info",
    )
)

VerifyDomain = domains.add(
    Endpoint(
        method=Method.POST,
        path="/<domain_id>/actions/verify",
        response=VerifyDomainResponse,
        name="verify_domain",
        summary="Trigger DNS verification for a domain",
    )
)

GetCertificateChain = domains.add(
    Endpoint(
        method=Method.GET,
        path="/<domain_id>/certificate",
        response=GetCertificateChainResponse,
        name="get_certificate_chain",
        summary="Fetch the full TLS certificate chain (PEM) for a domain",
    )
)

RenewCertificate = domains.add(
    Endpoint(
        method=Method.POST,
        path="/<domain_id>/actions/renew-certificate",
        response=RenewCertificateResponse,
        name="renew_certificate",
        summary="Force renewal of the TLS certificate for a domain",
    )
)

DeleteDomain = domains.add(
    Endpoint(
        method=Method.DELETE,
        path="/<domain_id>",
        response=DeleteDomainResponse,
        name="delete_domain",
        summary="Unregister a domain",
    )
)
