from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

__all__ = [
    "WhitelistEntry",
    "RouteDeclaration",
    "RoutesResponse",
]

MatchMode = Literal["exact", "exact_or_prefix", "prefix"]


class WhitelistEntry(BaseModel):
    path: str = Field(
        description="The path to exempt from JWT validation.",
        examples=["/my-agent/health", "/my-agent/public/"],
    )
    match: MatchMode = Field(
        default="exact",
        description=(
            "How the path is matched against incoming requests. "
            '"exact" matches the path exactly; '
            '"exact_or_prefix" matches the path itself or any sub-path; '
            '"prefix" matches only strict sub-paths (not the path itself).'
        ),
        examples=["exact", "prefix"],
    )


class RouteDeclaration(BaseModel):
    prefix: str = Field(
        description=(
            "URL prefix this agent owns. "
            "Cannot be '/' or '/*', and must not overlap with controlplane or authz prefixes. "
            "The prefix is stripped from requests before they reach the agent."
        ),
        examples=["/my-agent"],
    )
    whitelist: list[WhitelistEntry] = Field(
        default_factory=list,
        description="Paths under this prefix that bypass JWT validation.",
    )


class RoutesResponse(BaseModel):
    routes: list[RouteDeclaration] = Field(
        description="All route prefixes and their optional whitelist entries.",
        examples=[
            [
                {
                    "prefix": "/my-agent",
                    "whitelist": [
                        {"path": "/my-agent/health"},
                        {"path": "/my-agent/public/", "match": "prefix"},
                    ],
                }
            ]
        ],
    )
