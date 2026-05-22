from __future__ import annotations

from typing import TypeAlias

from press_api_spec.tier2_proxy_service_v2.base import Endpoint, EndpointGroup, Method
from press_api_spec.tier2_proxy_service_v2.models.cache import FlushResponse

__all__ = ["CacheGroup", "FlushDomain", "FlushAll"]

CacheGroup = EndpointGroup(prefix="/proxy", tags=("Cache",))


class FlushDomain(Endpoint):
    method = Method.POST
    path = "/flush/<domain>"
    name = "flush_domain"
    summary = "Flush all shared dict + worker local caches for a domain"
    Response: TypeAlias = FlushResponse


CacheGroup.add(FlushDomain)


class FlushAll(Endpoint):
    method = Method.POST
    path = "/flush"
    name = "flush_all"
    summary = "Flush all shared dicts and increment global version to force local LRU cache flushes"
    Response: TypeAlias = FlushResponse


CacheGroup.add(FlushAll)
