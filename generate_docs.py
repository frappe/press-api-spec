"""Generate OpenAPI 3.1 JSON specs for all Press API services and write a
multi-spec Swagger UI index.

Usage:
    python generate_docs.py
    # then open docs/index.html in a browser

To add a new service, append an entry to SERVICES below.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from press_api_spec.bench_manager_service_v1 import (
    ALL_ENDPOINTS as BENCH_MANAGER_ENDPOINTS,
)
from press_api_spec.compute_service_v1 import ALL_ENDPOINTS as COMPUTE_ENDPOINTS
from press_api_spec.compute_service_v1.base import (
    EmptyResponse,
    Endpoint,
    ErrorResponse,
)
from press_api_spec.node_agent_contract_v1 import ALL_ENDPOINTS as NODE_AGENT_CONTRACT_ENDPOINTS
from press_api_spec.node_agent_service_v1 import ALL_ENDPOINTS as NODE_AGENT_ENDPOINTS
from press_api_spec.proxy_service_v1 import ALL_ENDPOINTS as PROXY_ENDPOINTS
from pydantic import BaseModel

DOCS_DIR = Path(__file__).parent / "docs"
HTML_FILE = DOCS_DIR / "index.html"

_PARAM_RE = re.compile(r"<(?:[a-zA-Z_]\w*:)?(?P<name>[a-zA-Z_]\w*)>")


@dataclass
class ServiceSpec:
    slug: str  # filename stem, e.g. "compute-service"  → docs/compute-service.json
    title: str  # display name in the dropdown
    version: str
    description: str
    endpoints: list[Endpoint[Any, Any]]


SERVICES: list[ServiceSpec] = [
    ServiceSpec(
        slug="compute-service-v1",
        title="Compute Service",
        version="0.1.0",
        description="REST API for managing stacks, containers and volumes.",
        endpoints=COMPUTE_ENDPOINTS,
    ),
    ServiceSpec(
        slug="proxy-service-v1",
        title="Proxy Service",
        version="0.1.0",
        description="REST API for domain registration, TLS management, and routing.",
        endpoints=PROXY_ENDPOINTS,
    ),
    ServiceSpec(
        slug="bench-manager-service-v1",
        title="Bench Manager Service",
        version="0.1.0",
        description="REST API for managing press benches and their dependencies.",
        endpoints=BENCH_MANAGER_ENDPOINTS,
    ),
    ServiceSpec(
        slug="node-agent-service-v1",
        title="Node Agent Service",
        version="0.1.0",
        description="REST API exposed by the Press node agent for health probing, agent discovery refresh, and authorization checks.",
        endpoints=NODE_AGENT_ENDPOINTS,
    ),
    ServiceSpec(
        slug="node-agent-contract-v1",
        title="Node Agent Contract",
        version="0.1.0",
        description="API that every node-agent-compatible agent must implement. Node Agent calls these endpoints to discover routes and check liveness.",
        endpoints=NODE_AGENT_CONTRACT_ENDPOINTS,
    ),
]


def main() -> None:
    DOCS_DIR.mkdir(exist_ok=True)

    # Remove any stale spec JSON files from previous runs
    known_slugs = {f"{svc.slug}.json" for svc in SERVICES}
    for old in DOCS_DIR.glob("*.json"):
        if old.name not in known_slugs:
            old.unlink()
            print(f"removed stale {old}")

    specs: list[tuple[ServiceSpec, dict[str, Any]]] = []
    for svc in SERVICES:
        schema_cache: dict[str, dict[str, Any]] = {}
        spec = build_spec(svc, schema_cache)
        out = DOCS_DIR / f"{svc.slug}.json"
        out.write_text(json.dumps(spec, indent=2))
        print(f"wrote {out}")
        specs.append((svc, spec))

    HTML_FILE.write_text(_html(specs))
    print(f"wrote {HTML_FILE}")
    print(f"\nopen {HTML_FILE}")


def build_spec(svc: ServiceSpec, schema_cache: dict[str, dict[str, Any]]) -> dict[str, Any]:
    paths: dict[str, Any] = {}

    for ep in svc.endpoints:
        opath = _path_to_openapi(ep.full_path or ep.path)
        method = ep.method.value.lower()

        operation: dict[str, Any] = {
            "operationId": ep.name,
            "summary": ep.summary,
            "tags": list(ep.tags),
            "parameters": _path_params(ep.full_path or ep.path) + _query_params(ep, schema_cache),
            "responses": {
                "200": _response_body(ep, schema_cache),
                **_error_responses(schema_cache),
            },
        }

        body = _request_body(ep, schema_cache)
        if body is not None:
            operation["requestBody"] = body

        paths.setdefault(opath, {})[method] = operation

    return {
        "openapi": "3.1.0",
        "info": {
            "title": svc.title,
            "version": svc.version,
            "description": svc.description,
        },
        "paths": paths,
        "components": {"schemas": schema_cache},
    }


def _collect_schemas(model: type[BaseModel], schema_cache: dict[str, dict[str, Any]]) -> None:
    full = model.model_json_schema(
        mode="serialization", ref_template="#/components/schemas/{model}"
    )
    defs = full.pop("$defs", {})
    for name, schema in defs.items():
        if name not in schema_cache:
            schema_cache[name] = schema
    name = model.__name__
    if name not in schema_cache:
        schema_cache[name] = full


def _ref(model: type[BaseModel], schema_cache: dict[str, dict[str, Any]]) -> dict[str, str]:
    _collect_schemas(model, schema_cache)
    return {"$ref": f"#/components/schemas/{model.__name__}"}


def _path_to_openapi(path: str) -> str:
    return _PARAM_RE.sub(lambda m: "{" + m.group("name") + "}", path)


def _path_params(path: str) -> list[dict[str, Any]]:
    return [
        {
            "name": m.group("name"),
            "in": "path",
            "required": True,
            "schema": {"type": "string"},
        }
        for m in _PARAM_RE.finditer(path)
    ]


def _query_params(
    ep: Endpoint[Any, Any], schema_cache: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    query = getattr(ep, "Query", None)
    if query is None:
        return []
    _collect_schemas(query, schema_cache)
    schema = query.model_json_schema(
        mode="serialization", ref_template="#/components/schemas/{model}"
    )
    defs = schema.pop("$defs", {})
    for name, s in defs.items():
        if name not in schema_cache:
            schema_cache[name] = s
    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    return [
        {
            "name": name,
            "in": "query",
            "required": name in required,
            "schema": prop_schema,
        }
        for name, prop_schema in props.items()
    ]


def _request_body(
    ep: Endpoint[Any, Any], schema_cache: dict[str, dict[str, Any]]
) -> dict[str, Any] | None:
    body = getattr(ep, "Body", None)
    if body is None:
        return None
    return {
        "required": True,
        "content": {"application/json": {"schema": _ref(body, schema_cache)}},
    }


def _response_body(
    ep: Endpoint[Any, Any], schema_cache: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    response = getattr(ep, "Response", None)
    if response is None or response is EmptyResponse:
        return {"description": "Success"}
    return {
        "description": "Success",
        "content": {"application/json": {"schema": _ref(response, schema_cache)}},
    }


def _error_responses(schema_cache: dict[str, dict[str, Any]]) -> dict[str, Any]:
    err = {
        "description": "Error",
        "content": {"application/json": {"schema": _ref(ErrorResponse, schema_cache)}},
    }
    return {
        "400": {**err, "description": "Bad request"},
        "401": {**err, "description": "Unauthorized"},
        "404": {**err, "description": "Not found"},
        "500": {**err, "description": "Internal server error"},
    }


def _deref(obj: Any, schemas: dict[str, Any], _visited: frozenset[str] = frozenset()) -> Any:
    """Recursively inline all #/components/schemas/$ref pointers."""
    if isinstance(obj, dict):
        if "$ref" in obj:
            ref: str = obj["$ref"]
            if ref.startswith("#/components/schemas/"):
                name = ref[len("#/components/schemas/") :]
                if name in _visited:
                    return obj  # break cycles
                return _deref(schemas[name], schemas, _visited | {name})
        return {k: _deref(v, schemas, _visited) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_deref(item, schemas, _visited) for item in obj]
    return obj


def _deref_spec(spec: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of *spec* with all $refs inlined (no components needed)."""
    schemas = spec.get("components", {}).get("schemas", {})
    dereffed = _deref(spec, schemas)
    dereffed.pop("components", None)  # no longer needed
    return dereffed


def _html(specs: list[tuple[ServiceSpec, dict[str, Any]]]) -> str:
    # Inline each spec as a JS variable to avoid CORS issues when opening as file://.
    # Specs are fully dereferenced so $ref resolution never hits the network or
    # the document URL (which breaks under file://).
    inline_vars = "\n".join(
        f"    const SPEC_{i} = {json.dumps(spec)};" for i, (_, spec) in enumerate(specs)
    )
    specs_js = (
        "["
        + ", ".join(
            f"{{slug: {json.dumps(svc.slug)}, name: {json.dumps(svc.title)}, spec: SPEC_{i}}}"
            for i, (svc, _) in enumerate(specs)
        )
        + "]"
    )
    page_title = "Press API Docs"
    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{page_title}</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
  <style>
    /* remove excess top space */
    .swagger-ui .info {{ margin: 20px 0 10px; }}
    /* keep h1 children on the same baseline */
    .info hgroup h1 {{ display: flex; align-items: center; flex-wrap: wrap; gap: 6px; }}
    .info hgroup h1 span {{ display: inline-flex; align-items: center; }}
    /* fix version badge vertical position */
    .info hgroup h1 span small {{ top: 0 !important; }}
    #svc-switcher {{
      display: inline-flex;
      align-items: center;
      margin-left: auto;
      position: relative;
    }}
    #svc-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      border: 1.5px solid #61affe;
      border-radius: 20px;
      background: #fff;
      color: #61affe;
      cursor: pointer;
      font-size: 13px;
      font-weight: 600;
      transition: background .15s, color .15s;
    }}
    #svc-btn:hover {{ background: #61affe; color: #fff; }}
    #svc-btn:hover svg path {{ stroke: #fff; }}
    #svc-btn svg {{ width: 15px; height: 15px; flex-shrink: 0; }}
    #json-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      border: 1.5px solid #fca130;
      border-radius: 20px;
      background: #fff;
      color: #fca130;
      cursor: pointer;
      font-size: 13px;
      font-weight: 600;
      transition: background .15s, color .15s;
      margin-left: 8px;
      text-decoration: none;
    }}
    #json-btn:hover {{ background: #fca130; color: #fff; }}
    #json-btn:hover svg path {{ stroke: #fff; }}
    #json-btn svg {{ width: 15px; height: 15px; flex-shrink: 0; }}
    #svc-menu {{
      display: none;
      position: absolute;
      top: calc(100% + 6px);
      right: 0;
      left: auto;
      background: #fff;
      border: 1px solid #d8dde7;
      border-radius: 6px;
      box-shadow: 0 4px 16px rgba(0,0,0,.12);
      min-width: 200px;
      z-index: 9999;
      overflow: hidden;
    }}
    #svc-menu.open {{ display: block; }}
    #svc-menu button {{
      display: block;
      width: 100%;
      text-align: left;
      padding: 9px 16px;
      font-size: 14px;
      background: none;
      border: none;
      cursor: pointer;
      color: #3b4151;
    }}
    #svc-menu button:hover {{ background: #f0f5ff; color: #61affe; }}
    #svc-menu button.active {{ font-weight: 700; color: #61affe; }}
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
  <script>
{inline_vars}
    const allSpecs = {specs_js};

    // Query-param based persistence: ?service=compute-service-v1
    function getSlugFromQuery() {{
      return new URLSearchParams(location.search).get("service");
    }}

    function indexForSlug(slug) {{
      const i = allSpecs.findIndex(s => s.slug === slug);
      return i >= 0 ? i : 0;
    }}

    function setQuerySlug(slug) {{
      const u = new URL(location.href);
      u.searchParams.set("service", slug);
      history.replaceState(null, "", u.toString());
    }}

    let currentIndex = indexForSlug(getSlugFromQuery() || allSpecs[0].slug);

    const isLocal = location.protocol === "file:"
      || location.hostname === "localhost"
      || location.hostname.endsWith(".localhost")
      || /^127\\./.test(location.hostname);

    const ui = SwaggerUIBundle({{
      spec: allSpecs[currentIndex].spec,
      dom_id: "#swagger-ui",
      presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset],
      layout: "BaseLayout",
      deepLinking: false,
      supportedSubmitMethods: isLocal ? ["get", "post", "put", "delete", "patch", "head", "options", "trace"] : [],
    }});

    function switchSpec(i) {{
      currentIndex = i;
      setQuerySlug(allSpecs[i].slug);
      ui.specActions.updateSpec(JSON.stringify(allSpecs[i].spec));
      renderSwitcher();
    }}

    function renderSwitcher() {{
      const menu = document.getElementById("svc-menu");
      if (!menu) return;
      menu.querySelectorAll("button").forEach((b, i) => {{
        b.classList.toggle("active", i === currentIndex);
      }});
    }}

    // Inject switcher into the h1 title line once Swagger UI has rendered
    const observer = new MutationObserver(() => {{
      const h1 = document.querySelector(".info hgroup h1");
      if (h1 && !document.getElementById("svc-switcher")) {{
        observer.disconnect();

        const switcher = document.createElement("span");
        switcher.id = "svc-switcher";

        const btn = document.createElement("button");
        btn.id = "svc-btn";
        btn.title = "Switch service";
        btn.innerHTML = 'Switch <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7 16H17M17 16L14 13M17 16L14 19M17 8H7M7 8L10 5M7 8L10 11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

        const menu = document.createElement("div");
        menu.id = "svc-menu";
        allSpecs.forEach((s, i) => {{
          const item = document.createElement("button");
          item.textContent = s.name;
          if (i === currentIndex) item.classList.add("active");
          item.addEventListener("click", () => {{
            menu.classList.remove("open");
            switchSpec(i);
          }});
          menu.appendChild(item);
        }});

        btn.addEventListener("click", e => {{
          e.stopPropagation();
          menu.classList.toggle("open");
        }});
        document.addEventListener("click", () => menu.classList.remove("open"));

        switcher.appendChild(btn);
        switcher.appendChild(menu);
        h1.appendChild(switcher);

        const jsonBtn = document.createElement("a");
        jsonBtn.id = "json-btn";
        jsonBtn.title = "Open OpenAPI JSON";
        jsonBtn.target = "_blank";
        jsonBtn.innerHTML = 'OpenAPI JSON <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 6h16M4 10h16M4 14h16M4 18h16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

        function updateJsonHref() {{
          jsonBtn.href = allSpecs[currentIndex].slug + ".json";
        }}
        updateJsonHref();

        // Override the original switchSpec to also update the JSON link
        const origSwitchSpec = switchSpec;
        switchSpec = function(i) {{
          origSwitchSpec(i);
          updateJsonHref();
        }};

        h1.appendChild(jsonBtn);
      }}
    }});
    observer.observe(document.getElementById("swagger-ui"), {{ childList: true, subtree: true }});
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
