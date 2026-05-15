from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Generic, Iterator, TypeVar

from pydantic import BaseModel
from typing_extensions import TypeVar as TypeVarExt

__all__ = [
    "Method",
    "Endpoint",
    "EndpointGroup",
    "PaginationParams",
    "PaginationInfo",
    "Paginated",
    "EmptyResponse",
    "ErrorCode",
    "ErrorDetail",
    "ErrorResponse",
]


class Method(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


T = TypeVar("T")


class PaginationParams(BaseModel):
    """Standard query parameters for a paginated list endpoint."""

    page: int = 1
    per_page: int = 20


class PaginationInfo(BaseModel):
    page: int
    per_page: int
    previous_page: int | None
    next_page: int | None
    last_page: int
    total_pages: int
    total_entries: int


class Paginated(BaseModel, Generic[T]):
    """Generic paginated envelope: ``Paginated[Instance]`` etc."""

    items: list[T]
    pagination: PaginationInfo


class EmptyResponse(BaseModel):
    """Use as ``response=EmptyResponse`` for endpoints with no payload."""

    pass


class ErrorCode(str, Enum):
    BAD_REQUEST = "bad_request"
    VALIDATION_FAILED = "validation_failed"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    QUOTA_EXCEEDED = "quota_exceeded"
    RATE_LIMITED = "rate_limited"
    ACTION_FAILED = "action_failed"
    INTERNAL_ERROR = "internal_error"


class ErrorDetail(BaseModel):
    code: ErrorCode
    message: str
    details: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail


BodyT = TypeVarExt("BodyT", bound=BaseModel, default=BaseModel)
ResponseT = TypeVarExt("ResponseT", bound=BaseModel, default=BaseModel)

_PATH_PARAM_RE = re.compile(r"<(?:(?P<conv>[a-zA-Z_]\w*):)?(?P<name>[a-zA-Z_]\w*)>")


@dataclass(frozen=True)
class Endpoint(Generic[BodyT, ResponseT]):
    """Declarative description of a single HTTP endpoint."""

    method: Method
    path: str
    body: type[BodyT] | None = None
    response: type[ResponseT] | None = None
    query: type[BaseModel] | None = None
    name: str = ""
    summary: str = ""
    tags: tuple[str, ...] = ()
    full_path: str = ""

    def path_params(self) -> list[str]:
        return [m.group("name") for m in _PATH_PARAM_RE.finditer(self.path)]

    def url(self, **params: Any) -> str:
        """Render the path by substituting ``<...>`` placeholders."""
        required = self.path_params()
        missing = [p for p in required if p not in params]
        if missing:
            raise KeyError(f"{self._label()}: missing path parameter(s) {missing}")

        def repl(match: re.Match[str]) -> str:
            return str(params[match.group("name")])

        return _PATH_PARAM_RE.sub(repl, self.path)

    def parse_body(self, data: Any) -> BodyT:
        if self.body is None:
            raise ValueError(f"{self._label()}: no body type defined")
        return self.body.model_validate(data)

    def parse_response(self, data: Any) -> ResponseT:
        if self.response is None:
            raise ValueError(f"{self._label()}: no response type defined")
        return self.response.model_validate(data)

    def parse_query(self, data: Any) -> BaseModel:
        if self.query is None:
            raise ValueError(f"{self._label()}: no query type defined")
        return self.query.model_validate(data)

    def _label(self) -> str:
        return self.name or f"{self.method.value} {self.path}"

    def __str__(self) -> str:
        return f"<Endpoint {self.method.value} {self.path}>"


@dataclass
class EndpointGroup:
    prefix: str = ""
    tags: tuple[str, ...] = ()
    endpoints: list[Endpoint[Any, Any]] = field(default_factory=list)

    def add(self, endpoint: Endpoint[BodyT, ResponseT]) -> Endpoint[BodyT, ResponseT]:
        if self.prefix:
            sub = endpoint.path.lstrip("/")
            prefixed_path = self.prefix.rstrip("/") + ("/" + sub if sub else "")
        else:
            prefixed_path = endpoint.path
        merged_tags = endpoint.tags or self.tags
        endpoint = Endpoint(
            method=endpoint.method,
            path=endpoint.path,
            body=endpoint.body,
            response=endpoint.response,
            query=endpoint.query,
            name=endpoint.name,
            summary=endpoint.summary,
            tags=merged_tags,
            full_path=prefixed_path,
        )
        self.endpoints.append(endpoint)
        return endpoint

    def __iter__(self) -> Iterator[Endpoint[Any, Any]]:
        return iter(self.endpoints)

    def __len__(self) -> int:
        return len(self.endpoints)
