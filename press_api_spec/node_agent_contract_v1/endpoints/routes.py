from __future__ import annotations

from typing import TypeAlias

from press_api_spec.base import Endpoint, EndpointGroup, Method
from press_api_spec.node_agent_contract_v1.models.routes import RoutesResponse

__all__ = ["MetaGroup", "GetRoutes"]


MetaGroup = EndpointGroup(prefix="/_meta", tags=("Meta",))


class GetRoutes(Endpoint):
    method = Method.GET
    path = "/routes"
    name = "get_routes"
    summary = "Return all route prefixes and whitelist entries the agent owns"
    Response: TypeAlias = RoutesResponse


MetaGroup.add(GetRoutes)
