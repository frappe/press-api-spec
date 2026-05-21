from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

from press_api_spec.proxy_service_v1.base import EmptyResponse, Paginated, PaginationParams

__all__ = [
    "DomainStatus",
    "TlsStatus",
    "DnsRecord",
    "TlsCertificate",
    "TlsCertificateChain",
    "Domain",
    "RegisterDomainRequest",
    "RegisterDomainResponse",
    "ListDomainsQuery",
    "ListDomainsResponse",
    "GetDomainResponse",
    "GetCertificateChainResponse",
    "VerifyDomainResponse",
    "RenewCertificateResponse",
    "DeleteDomainResponse",
]


class DomainStatus(str, Enum):
    PENDING = "pending"
    VERIFYING = "verifying"
    VERIFIED = "verified"
    ACTIVE = "active"
    ERROR = "error"


class DnsRecord(BaseModel):
    type: str = Field(examples=["A", "CNAME"])
    name: str = Field(examples=["api.example.com", "@"])
    value: str = Field(examples=["203.0.113.1", "proxy.press.dev"])
    ttl: int = 300


class TlsStatus(str, Enum):
    PENDING = "pending"
    PROVISIONING = "provisioning"
    ACTIVE = "active"
    EXPIRED = "expired"
    ERROR = "error"


class TlsCertificate(BaseModel):
    issuer: str | None = None
    issued_at_unix: int | None = None
    expires_at_unix: int | None = None
    status: TlsStatus = TlsStatus.PENDING


class TlsCertificateChain(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "domain_id": "dom_abc123",
                    "certificate_pem": "-----BEGIN CERTIFICATE-----\nMIID...\n-----END CERTIFICATE-----\n",
                    "chain_pem": "-----BEGIN CERTIFICATE-----\nMIIE...\n-----END CERTIFICATE-----\n",
                    "fullchain_pem": "-----BEGIN CERTIFICATE-----\nMIID...\nMIIE...\n-----END CERTIFICATE-----\n",
                    "issuer": "Let's Encrypt",
                    "issued_at_unix": 1736899200,
                    "expires_at_unix": 1744675200,
                }
            ]
        }
    )

    domain_id: str
    certificate_pem: str
    chain_pem: str
    fullchain_pem: str
    issuer: str | None = None
    issued_at_unix: int | None = None
    expires_at_unix: int | None = None


class Domain(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "dom_abc123",
                    "domain": "api.example.com",
                    "status": "active",
                    "dns_records": [
                        {"type": "A", "name": "api.example.com", "value": "203.0.113.1", "ttl": 300}
                    ],
                    "tls_certificate": {
                        "issuer": "Let's Encrypt",
                        "issued_at_unix": 1736899200,
                        "expires_at_unix": 1744675200,
                        "status": "active",
                    },
                    "verified_at_unix": 1736942400,
                    "error_message": None,
                    "created_at_unix": 1736935200,
                    "updated_at_unix": 1736942400,
                }
            ]
        }
    )

    id: str
    domain: str
    status: DomainStatus = DomainStatus.PENDING
    dns_records: list[DnsRecord] = []
    tls_certificate: TlsCertificate = TlsCertificate()
    verified_at_unix: int | None = None
    error_message: str | None = None
    created_at_unix: int
    updated_at_unix: int


class RegisterDomainRequest(BaseModel):
    domain: str = Field(examples=["api.example.com", "*.example.com"])


class RegisterDomainResponse(BaseModel):
    domain: Domain


class ListDomainsQuery(PaginationParams):
    status: DomainStatus | None = None
    domain: str | None = Field(default=None, examples=["example.com"])


ListDomainsResponse = Paginated[Domain]


class GetDomainResponse(BaseModel):
    domain: Domain


class GetCertificateChainResponse(BaseModel):
    certificate: TlsCertificateChain


class VerifyDomainResponse(BaseModel):
    domain: Domain


class RenewCertificateResponse(BaseModel):
    domain: Domain


DeleteDomainResponse = EmptyResponse
