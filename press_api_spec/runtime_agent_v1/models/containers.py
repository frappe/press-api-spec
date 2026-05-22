from __future__ import annotations

from pydantic import BaseModel

__all__ = ["RestartContainerResponse"]


class RestartContainerResponse(BaseModel):
    status: str
    message: str
