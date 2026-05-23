from __future__ import annotations

from pydantic import BaseModel, Field

from press_api_spec.tier1_proxy_service_v1.base import EmptyResponse

__all__ = [
    "Tier1SetChallengeRequest",
    "Tier1SetChallengeResponse",
    "Tier1DeleteChallengeResponse",
]


class Tier1SetChallengeRequest(BaseModel):
    token: str = Field(description="ACME http-01 challenge token")
    key_auth: str = Field(description="ACME key authorization value")


class Tier1SetChallengeResponse(BaseModel):
    status: str = "success"


Tier1DeleteChallengeResponse = EmptyResponse
