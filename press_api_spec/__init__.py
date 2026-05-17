"""press_api_spec -- API specifications for the Press platform.

Usage::

    from press_api_spec import compute_service_v1
    from press_api_spec import proxy_service_v1
    from press_api_spec import node_agent_service_v1
"""

from press_api_spec import compute_service_v1
from press_api_spec import node_agent_service_v1
from press_api_spec import proxy_service_v1

__all__ = ["compute_service_v1", "node_agent_service_v1", "proxy_service_v1"]
