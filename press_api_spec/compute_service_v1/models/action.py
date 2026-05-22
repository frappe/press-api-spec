from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = [
    "RuntimeAgentActionResponse",
]


class RuntimeAgentActionResponse(BaseModel):
    status: str = Field(default="accepted", examples=["accepted"])
    restarted: int = Field(default=0, examples=[1])
