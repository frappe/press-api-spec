from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = [
    "RefreshAgentQuery",
    "RefreshAgentResponse",
    "CheckResource",
    "CheckRequest",
    "HasPermissionResponse",
]


class RefreshAgentQuery(BaseModel):
    agent: str | None = Field(
        default=None,
        description="Agent name to refresh. Omit to refresh all agents.",
        examples=["my-agent"],
    )


class RefreshAgentResponse(BaseModel):
    refreshed: str = Field(
        description='Name of the refreshed agent, or "all" when no agent was specified.',
        examples=["my-agent", "all"],
    )


class CheckResource(BaseModel):
    type: str = Field(description="Resource type.", examples=["site"])
    id: str = Field(description="Resource identifier.", examples=["abc123"])


class CheckRequest(BaseModel):
    sub: str = Field(description="Subject (user identifier) from the JWT.", examples=["user-1"])
    jti: str = Field(description="JWT ID (unique token identifier).", examples=["tok-xyz"])
    resource: CheckResource
    action: str = Field(description="Action being performed.", examples=["read", "write"])


class HasPermissionResponse(BaseModel):
    allowed: bool = Field(description="Whether the action is permitted.")
