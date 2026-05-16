from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from press_api_spec.compute_service_v1.base import EmptyResponse

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
    model_config = ConfigDict(json_schema_extra={"examples": [{"app_name": "erpnext"}]})

    app_name: str = Field(examples=["erpnext"])


class AppWebhookRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "app": "erpnext",
                    "github_installation_id": "12345678",
                    "orginisation": "frappe",
                    "repository": "erpnext",
                    "branch": "version-15",
                    "event": "push",
                    "data": {"key": "value"},
                    "team": "developers",
                    "is_public": "True",
                }
            ]
        }
    )

    app: str = Field(examples=["erpnext"])
    github_installation_id: str = Field(
        description="GitHub App installation ID.",
        examples=["12345678"],
    )
    orginisation: str = Field(examples=["frappe"])
    repository: str = Field(examples=["erpnext"])
    branch: str = Field(examples=["version-15", "main", "develop"])
    event: str = Field(examples=["push", "pull_request"])
    data: dict = Field(description="Event payload data.", examples=[{"key": "value"}])
    team: str = Field(examples=["developers"])
    is_public: str = Field(
        description="Used for marketplace apps",
        examples=["True", "False"],
    )


class AppWebhookResponse(BaseModel):
    message: str = Field(examples=["Webhook received successfully"])


class RemoveAppResponse(BaseModel):
    message: str = Field(examples=["erpnext removed successfully"])


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])
