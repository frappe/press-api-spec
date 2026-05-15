from __future__ import annotations

from typing import TypeAlias

from press_api_spec.bench_manager_service_v1.models.bench import (
    DeleteExternalBenchPackagesRequest,
    DeleteExternalBenchPackagesResponse,
    UpdateBenchDependenciesRequest,
    UpdateBenchDependenciesResponse,
    UpdateBuildStatusRequest,
    UpdateExternalBenchPackagesRequest,
    UpdateExternalBenchPackagesResponse,
)
from press_api_spec.compute_service_v1.base import Endpoint, EndpointGroup, Method

__all__ = [
    "BenchGroup",
    "UpdateBenchDependencies",
    "AddExternalBenchPackages",
    "DeleteExternalBenchPackages",
    "UpdateBuildStatus",
]


BenchGroup = EndpointGroup(
    prefix="/bench",
    tags=("Bench",),
)

class UpdateBenchDependencies(Endpoint):
    method = Method.PUT
    path = "/dependencies"
    name = "update_bench_dependencies"
    summary = "Replace the full set of bench dependency versions (Node, Python, etc.)"
    Body: TypeAlias = UpdateBenchDependenciesRequest
    Response: TypeAlias = UpdateBenchDependenciesResponse

BenchGroup.add(UpdateBenchDependencies)

class AddExternalBenchPackages(Endpoint):
    method = Method.POST
    path = "/external-packages"
    name = "add_external_bench_packages"
    summary = "Add external system packages (e.g. apt) to the bench"
    Body: TypeAlias = UpdateExternalBenchPackagesRequest
    Response: TypeAlias = UpdateExternalBenchPackagesResponse

BenchGroup.add(AddExternalBenchPackages)

class DeleteExternalBenchPackages(Endpoint):
    method = Method.DELETE
    path = "/external-packages"
    name = "delete_external_bench_packages"
    summary = "Remove external system packages from the bench"
    Body: TypeAlias = DeleteExternalBenchPackagesRequest
    Response: TypeAlias = DeleteExternalBenchPackagesResponse

BenchGroup.add(DeleteExternalBenchPackages)

class UpdateBuildStatus(Endpoint):
    method = Method.POST
    path = "/builds/update"
    name = "update_build_status"
    summary = "Receive a build status callback from the CI/build system"
    Body: TypeAlias = UpdateBuildStatusRequest

BenchGroup.add(UpdateBuildStatus)
