from __future__ import annotations

import typing

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "BenchDependencyName",
    "BenchDependency",
    "UpdateBenchDependenciesRequest",
    "UpdateBenchDependenciesResponse",
    "ExternalPackageManager",
    "ExternalBenchPackage",
    "UpdateExternalBenchPackagesRequest",
    "UpdateExternalBenchPackagesResponse",
    "DeleteExternalBenchPackagesRequest",
    "DeleteExternalBenchPackagesResponse",
    "UpdateBuildStatusRequest",
]

BenchDependencyName = typing.Literal[
    "NVM_VERSION",
    "PYTHON_VERSION",
    "NODE_VERSION",
    "WKHTMLTOPDF_VERSION",
    "PIP_VERSION",
    "BENCH_VERSION",
]

ExternalPackageManager = typing.Literal["apt"]


class BenchDependency(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"dependency": "NODE_VERSION", "version": "20.11.0"},
                {"dependency": "PYTHON_VERSION", "version": "3.11.6"},
            ]
        }
    )

    dependency: BenchDependencyName
    version: str = Field(examples=["20.11.0", "3.11.6", "23.3.1"])


class UpdateBenchDependenciesRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "dependencies": [
                        {"dependency": "NODE_VERSION", "version": "20.11.0"},
                        {"dependency": "PYTHON_VERSION", "version": "3.11.6"},
                    ]
                }
            ]
        }
    )

    dependencies: list[BenchDependency]


class UpdateBenchDependenciesResponse(BaseModel):
    message: str = Field(examples=["Dependencies updated successfully"])


class ExternalBenchPackage(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"manager": "apt", "package": "libpq-dev"},
                {"manager": "apt", "package": "wkhtmltopdf"},
            ]
        }
    )

    manager: ExternalPackageManager
    package: str = Field(examples=["libpq-dev", "wkhtmltopdf", "redis-tools"])


class UpdateExternalBenchPackagesRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "external_packages": [
                        {"manager": "apt", "package": "libpq-dev"},
                        {"manager": "apt", "package": "wkhtmltopdf"},
                    ]
                }
            ]
        }
    )

    external_packages: list[ExternalBenchPackage]


class UpdateExternalBenchPackagesResponse(BaseModel):
    message: str = Field(examples=["Packages updated successfully"])


# Semantically identical payload, aliased for endpoint clarity
DeleteExternalBenchPackagesRequest = UpdateExternalBenchPackagesRequest


class DeleteExternalBenchPackagesResponse(BaseModel):
    message: str = Field(examples=["Packages updated successfully"])


class BuildStatus(str):
    pass


class UpdateBuildStatusRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "job_id": "build_abc123",
                    "status": "success",
                    "output": "Build completed in 42s",
                },
                {
                    "job_id": "build_abc123",
                    "status": "failed",
                    "output": "Error: package not found",
                },
            ]
        }
    )

    job_id: str = Field(examples=["build_abc123"])
    status: str = Field(examples=["success", "failed", "running"])
    output: str | None = Field(default=None, examples=["Build completed in 42s"])