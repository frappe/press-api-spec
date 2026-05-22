from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = ["FlushResponse"]


class FlushResponse(BaseModel):
    status: str = Field(default="success", description="Status code")
