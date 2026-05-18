from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = ["HealthResponse"]


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])
    service: str = Field(examples=["node-agent-service-v1"])
    version: str = Field(examples=["0.1.0"])
    time: int
