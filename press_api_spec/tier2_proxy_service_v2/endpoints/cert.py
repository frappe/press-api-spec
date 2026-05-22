from __future__ import annotations

from typing import TypeAlias

from press_api_spec.tier2_proxy_service_v2.base import Endpoint, EndpointGroup, Method
from press_api_spec.tier2_proxy_service_v2.models.cert import (
    DeleteCertResponse,
    DeleteChallengeResponse,
    SetCertRequest,
    SetCertResponse,
    SetChallengeRequest,
    SetChallengeResponse,
)

__all__ = [
    "CertGroup",
    "SetCert",
    "DeleteCert",
    "SetChallenge",
    "DeleteChallenge",
]

CertGroup = EndpointGroup(prefix="/proxy/certs", tags=("Certificates",))


class SetCert(Endpoint):
    method = Method.PUT
    path = "/<domain>"
    name = "set_cert"
    summary = "Validate and upload PEM certificates for a domain"
    Body: TypeAlias = SetCertRequest
    Response: TypeAlias = SetCertResponse


CertGroup.add(SetCert)


class DeleteCert(Endpoint):
    method = Method.DELETE
    path = "/<domain>"
    name = "delete_cert"
    summary = "Delete certificate for a domain"
    Response: TypeAlias = DeleteCertResponse


CertGroup.add(DeleteCert)


class SetChallenge(Endpoint):
    method = Method.PUT
    path = "/<domain>/challenge"
    name = "set_challenge"
    summary = "Set ACME http-01 challenge token for domain"
    Body: TypeAlias = SetChallengeRequest
    Response: TypeAlias = SetChallengeResponse


CertGroup.add(SetChallenge)


class DeleteChallenge(Endpoint):
    method = Method.DELETE
    path = "/<domain>/challenge/<token>"
    name = "delete_challenge"
    summary = "Delete ACME challenge token for domain"
    Response: TypeAlias = DeleteChallengeResponse


CertGroup.add(DeleteChallenge)
