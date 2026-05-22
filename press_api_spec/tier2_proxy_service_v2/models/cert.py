from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = [
    "SetCertRequest",
    "SetCertResponse",
    "DeleteCertResponse",
    "SetChallengeRequest",
    "SetChallengeResponse",
    "DeleteChallengeResponse",
]


class SetCertRequest(BaseModel):
    crt: str = Field(description="PEM formatted certificate chain")
    key: str = Field(description="PEM formatted private key")


class SetCertResponse(BaseModel):
    status: str = Field(default="success", description="Status code")


class DeleteCertResponse(BaseModel):
    status: str = Field(default="success", description="Status code")


class SetChallengeRequest(BaseModel):
    token: str = Field(description="ACME challenge token string")
    key_auth: str = Field(description="ACME key authorization string")


class SetChallengeResponse(BaseModel):
    status: str = Field(default="success", description="Status code")


class DeleteChallengeResponse(BaseModel):
    status: str = Field(default="success", description="Status code")
