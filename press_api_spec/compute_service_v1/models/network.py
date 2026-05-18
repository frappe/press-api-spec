from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from press_api_spec.compute_service_v1.base import (
    EmptyResponse,
    Paginated,
    PaginationParams,
)

__all__ = [
    "Network",
    "CreateNetworkRequest",
    "CreateNetworkResponse",
    "GetNetworkResponse",
    "ListNetworksQuery",
    "ListNetworksResponse",
    "UpdateNetworkRequest",
    "UpdateNetworkResponse",
    "DeleteNetworkResponse",
]


class Network(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "net_abc123",
                    "name": "production-overlay",
                    "description": "Overlay network for production workloads",
                    "cidr": "10.0.0.0/16",
                    "gateway_ip": "10.0.0.1",
                    "created_at_unix": 1736935200,
                    "updated_at_unix": 1736942400,
                },
                {
                    "id": "net_def456",
                    "name": "staging",
                    "description": "Staging environment overlay network",
                    "cidr": "10.1.0.0/16",
                    "gateway_ip": "10.1.0.1",
                    "created_at_unix": 1736949600,
                    "updated_at_unix": 1736956800,
                },
            ]
        }
    )

    id: str = Field(description="Server-generated unique identifier")
    name: str = Field(examples=["production-overlay", "staging"], description="User-provided network name")
    description: str | None = Field(default=None, examples=["Overlay network for production workloads"])
    cidr: str = Field(
        examples=["10.0.0.0/16", "10.1.0.0/16"],
        description="CIDR block for the network address space",
    )
    gateway_ip: str = Field(
        examples=["10.0.0.1", "10.1.0.1"],
        description="Gateway IP address within the CIDR block",
    )
    created_at_unix: int = Field(description="UTC timestamp in seconds since epoch")
    updated_at_unix: int = Field(description="UTC timestamp in seconds since epoch")


class CreateNetworkRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "production-overlay",
                    "description": "Overlay network for production workloads",
                    "cidr": "10.0.0.0/16",
                },
                {
                    "name": "staging",
                    "description": "Staging environment overlay network",
                    "cidr": "10.1.0.0/16",
                },
            ]
        }
    )

    name: str = Field(examples=["production-overlay", "staging"])
    description: str | None = Field(default=None, examples=["Overlay network for production workloads"])
    cidr: str = Field(examples=["10.0.0.0/16", "10.1.0.0/16"])


class CreateNetworkResponse(BaseModel):
    network: Network


class ListNetworksQuery(PaginationParams):
    name: str | None = Field(default=None, examples=["production-overlay"])


ListNetworksResponse = Paginated[Network]


class GetNetworkResponse(BaseModel):
    network: Network


class UpdateNetworkRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"description": "Updated network description"},
                {"name": "prod-overlay-v2"},
            ]
        }
    )

    name: str | None = Field(default=None, examples=["prod-overlay-v2"])
    description: str | None = Field(default=None, examples=["Updated network description"])


class UpdateNetworkResponse(BaseModel):
    network: Network


DeleteNetworkResponse = EmptyResponse
