from __future__ import annotations

from typing import TypeAlias

from press_api_spec.tier1_proxy_service_v1.base import Endpoint, EndpointGroup, Method
from press_api_spec.tier1_proxy_service_v1.models.cert import (
    Tier1DeleteChallengeResponse,
    Tier1SetChallengeRequest,
    Tier1SetChallengeResponse,
)

__all__ = [
    "Tier1CertGroup",
    "Tier1SetChallenge",
    "Tier1DeleteChallenge",
]

Tier1CertGroup = EndpointGroup(prefix="/proxy/certs", tags=("Certificates",))


class Tier1SetChallenge(Endpoint):
    method = Method.PUT
    path = "/<domain>/challenge"
    name = "set_challenge"
    summary = "Store an ACME http-01 challenge token in T1 Redis"
    Body: TypeAlias = Tier1SetChallengeRequest
    Response: TypeAlias = Tier1SetChallengeResponse


Tier1CertGroup.add(Tier1SetChallenge)


class Tier1DeleteChallenge(Endpoint):
    method = Method.DELETE
    path = "/<domain>/challenge/<token>"
    name = "delete_challenge"
    summary = "Remove an ACME http-01 challenge token from T1 Redis"
    Response: TypeAlias = Tier1DeleteChallengeResponse


Tier1CertGroup.add(Tier1DeleteChallenge)
