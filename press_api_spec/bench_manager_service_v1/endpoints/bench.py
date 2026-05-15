from __future__ import annotations

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
    "bench",
    "UpdateBenchDependencies",
    "AddExternalBenchPackages",
    "DeleteExternalBenchPackages",
    "UpdateBuildStatus",
]


bench = EndpointGroup(
    prefix="/bench",
    tags=("Bench",),
)

UpdateBenchDependencies = bench.add(
    Endpoint(
        method=Method.PUT,
        path="/dependencies",
        body=UpdateBenchDependenciesRequest,
        response=UpdateBenchDependenciesResponse,
        name="update_bench_dependencies",
        summary="Replace the full set of bench dependency versions (Node, Python, etc.)",
    )
)

AddExternalBenchPackages = bench.add(
    Endpoint(
        method=Method.POST,
        path="/external-packages",
        body=UpdateExternalBenchPackagesRequest,
        response=UpdateExternalBenchPackagesResponse,
        name="add_external_bench_packages",
        summary="Add external system packages (e.g. apt) to the bench",
    )
)

DeleteExternalBenchPackages = bench.add(
    Endpoint(
        method=Method.DELETE,
        path="/external-packages",
        body=DeleteExternalBenchPackagesRequest,
        response=DeleteExternalBenchPackagesResponse,
        name="delete_external_bench_packages",
        summary="Remove external system packages from the bench",
    )
)

UpdateBuildStatus = bench.add(
    Endpoint(
        method=Method.POST,
        path="/builds/update",
        body=UpdateBuildStatusRequest,
        response=None,
        name="update_build_status",
        summary="Receive a build status callback from the CI/build system",
    )
)
