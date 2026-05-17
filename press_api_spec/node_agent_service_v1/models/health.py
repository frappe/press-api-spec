from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = ["HealthResponse"]


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])
