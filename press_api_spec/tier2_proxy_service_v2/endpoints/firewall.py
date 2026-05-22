from __future__ import annotations

from typing import TypeAlias

from press_api_spec.tier2_proxy_service_v2.base import Endpoint, EndpointGroup, Method
from press_api_spec.tier2_proxy_service_v2.models.firewall import (
    BlockIpRequest,
    BlockIpResponse,
    SetFirewallEnabledRequest,
    SetFirewallEnabledResponse,
    UnblockIpResponse,
)

__all__ = [
    "FirewallGroup",
    "SetFirewallEnabled",
    "BlockIp",
    "UnblockIp",
]

FirewallGroup = EndpointGroup(prefix="/proxy/firewall", tags=("Firewall",))


class SetFirewallEnabled(Endpoint):
    method = Method.PUT
    path = "/<domain>/enabled"
    name = "set_firewall_enabled"
    summary = "Enable or disable firewall checks for a domain"
    Body: TypeAlias = SetFirewallEnabledRequest
    Response: TypeAlias = SetFirewallEnabledResponse


FirewallGroup.add(SetFirewallEnabled)


class BlockIp(Endpoint):
    method = Method.POST
    path = "/<domain>/block"
    name = "block_ip"
    summary = "Block client IP address for a domain"
    Body: TypeAlias = BlockIpRequest
    Response: TypeAlias = BlockIpResponse


FirewallGroup.add(BlockIp)


class UnblockIp(Endpoint):
    method = Method.DELETE
    path = "/<domain>/block/<ip>"
    name = "unblock_ip"
    summary = "Unblock IP address for a domain"
    Response: TypeAlias = UnblockIpResponse


FirewallGroup.add(UnblockIp)
