from __future__ import annotations

from press_api_spec.compute_service_v1.base import EmptyResponse
from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "AddAppRequest",
    "AddAppResponse",
    "RemoveAppRequest",
    "RemoveAppResponse",
    "HealthResponse",
    "EmptyResponse",
]


class AddAppRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "repo_url": "https://github.com/frappe/erpnext",
                    "branch": "version-15",
                    "github_installation_id": "12345678",
                    "is_public": False,
                },
                {
                    "repo_url": "https://github.com/frappe/frappe",
                    "branch": "version-15",
                    "github_installation_id": None,
                    "is_public": True,
                },
            ]
        }
    )

    repo_url: str = Field(examples=["https://github.com/frappe/erpnext"])
    branch: str = Field(examples=["version-15", "main", "develop"])
    github_installation_id: str | None = Field(
        default=None,
        description="GitHub App installation ID. None for public repositories.",
        examples=["12345678"],
    )
    is_public: bool = Field(
        description="Whether the repository is publicly accessible.",
        examples=[True, False],
    )


class AddAppResponse(BaseModel):
    message: str = Field(examples=["erpnext added successfully"])


class RemoveAppRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "repo_url": "https://github.com/frappe/erpnext",
                    "branch": "version-15",
                }
            ]
        }
    )

    repo_url: str = Field(examples=["https://github.com/frappe/erpnext"])
    branch: str = Field(examples=["version-15", "main", "develop"])


class RemoveAppResponse(BaseModel):
    message: str = Field(examples=["erpnext removed successfully"])


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])
