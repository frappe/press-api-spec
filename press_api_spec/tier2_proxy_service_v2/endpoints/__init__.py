from __future__ import annotations

from press_api_spec.tier2_proxy_service_v2.endpoints.cache import (
    CacheGroup,
    FlushAll,
    FlushDomain,
)
from press_api_spec.tier2_proxy_service_v2.endpoints.cert import (
    CertGroup,
    DeleteCert,
    DeleteChallenge,
    SetCert,
    SetChallenge,
)
from press_api_spec.tier2_proxy_service_v2.endpoints.firewall import (
    BlockIp,
    FirewallGroup,
    SetFirewallEnabled,
    UnblockIp,
)
from press_api_spec.tier2_proxy_service_v2.endpoints.route import (
    DeleteRoute,
    RouteGroup,
    SetRoute,
)

ALL_ENDPOINTS = [
    SetRoute,
    DeleteRoute,
    SetCert,
    DeleteCert,
    SetChallenge,
    DeleteChallenge,
    SetFirewallEnabled,
    BlockIp,
    UnblockIp,
    FlushDomain,
    FlushAll,
]

ALL_GROUPS = [
    RouteGroup,
    CertGroup,
    FirewallGroup,
    CacheGroup,
]

__all__ = [
    "ALL_ENDPOINTS",
    "ALL_GROUPS",
    "RouteGroup",
    "SetRoute",
    "DeleteRoute",
    "CertGroup",
    "SetCert",
    "DeleteCert",
    "SetChallenge",
    "DeleteChallenge",
    "FirewallGroup",
    "SetFirewallEnabled",
    "BlockIp",
    "UnblockIp",
    "CacheGroup",
    "FlushDomain",
    "FlushAll",
]
