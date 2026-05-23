from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

from press_api_spec.proxy_service_v1.base import EmptyResponse, Paginated, PaginationParams

__all__ = [
    "DnsProvider",
    "RootDomain",
    "ConfigureRootDomainRequest",
    "ConfigureRootDomainResponse",
    "ListRootDomainsQuery",
    "ListRootDomainsResponse",
    "GetRootDomainResponse",
    "DeleteRootDomainResponse",
]


class DnsProvider(str, Enum):
    ROUTE53 = "route53"
    CLOUDFLARE = "cloudflare"


class RootDomain(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "example.com",
                    "root_domain": "example.com",
                    "dns_provider": "cloudflare",
                    "cloudflare_email": "admin@example.com",
                    "created_at_unix": 1736935200,
                    "updated_at_unix": 1736942400,
                }
            ]
        }
    )

    id: str
    root_domain: str
    dns_provider: DnsProvider
    cloudflare_email: str | None = None
    route53_region: str | None = None
    created_at_unix: int
    updated_at_unix: int


class ConfigureRootDomainRequest(BaseModel):
    root_domain: str = Field(examples=["example.com"])
    dns_provider: DnsProvider
    cloudflare_token: str | None = None
    cloudflare_email: str | None = None
    route53_access_key: str | None = None
    route53_secret_key: str | None = None
    route53_region: str | None = None


class ConfigureRootDomainResponse(BaseModel):
    root_domain: RootDomain


class ListRootDomainsQuery(PaginationParams):
    dns_provider: DnsProvider | None = None


ListRootDomainsResponse = Paginated[RootDomain]


class GetRootDomainResponse(BaseModel):
    root_domain: RootDomain


DeleteRootDomainResponse = EmptyResponse
