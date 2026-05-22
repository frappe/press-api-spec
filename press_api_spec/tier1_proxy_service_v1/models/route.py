from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = ["Tier1Route"]


class Tier1Route(BaseModel):
    domain: str = Field(description="Domain name registered in cluster routes")
    target: str = Field(description="Target Tier 2 proxy host:port address, e.g. t2-proxy:443")
