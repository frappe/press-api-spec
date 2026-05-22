from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = [
    "SetFirewallEnabledRequest",
    "SetFirewallEnabledResponse",
    "BlockIpRequest",
    "BlockIpResponse",
    "UnblockIpResponse",
]


class SetFirewallEnabledRequest(BaseModel):
    enabled: bool = Field(description="Enable/disable firewall state")


class SetFirewallEnabledResponse(BaseModel):
    status: str = Field(default="success", description="Status code")


class BlockIpRequest(BaseModel):
    ip: str = Field(description="Client IP address to block")


class BlockIpResponse(BaseModel):
    status: str = Field(default="success", description="Status code")


class UnblockIpResponse(BaseModel):
    status: str = Field(default="success", description="Status code")
