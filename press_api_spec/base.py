from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, ClassVar, Generic, Iterator, TypeVar, cast

from pydantic import BaseModel

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
    items: list[T]
    pagination: PaginationInfo


class EmptyResponse(BaseModel):
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


_PATH_PARAM_RE = re.compile(r"<(?:(?P<conv>[a-zA-Z_]\w*):)?(?P<name>[a-zA-Z_]\w*)>")


class EndpointMeta(type):
    def __call__(
        cls,
        method: Method,
        path: str,
        *,
        body: type[BaseModel] | None = None,
        response: type[BaseModel] | None = None,
        query: type[BaseModel] | None = None,
        name: str = "",
        summary: str = "",
        tags: tuple[str, ...] = (),
    ) -> type[Endpoint]:
        attrs: dict[str, Any] = {
            "method": method,
            "path": path,
            "name": name,
            "summary": summary,
            "tags": tags,
            "full_path": "",
        }
        if body is not None:
            attrs["Body"] = body
        if response is not None:
            attrs["Response"] = response
        if query is not None:
            attrs["Query"] = query
        return cast("type[Endpoint]", EndpointMeta(name or "Endpoint", (cls,), attrs))

    def __repr__(cls) -> str:
        if cls is Endpoint:
            return "<class 'Endpoint'>"
        method = getattr(cls, "method", None)
        path = getattr(cls, "path", "")
        if method is None:
            return f"<Endpoint {path}>"
        return f"<Endpoint {method.value} {path}>"

    def __class_getitem__(cls, item: Any) -> type:
        return cls


class Endpoint(metaclass=EndpointMeta):
    method: ClassVar[Method]
    path: ClassVar[str] = ""
    name: ClassVar[str] = ""
    summary: ClassVar[str] = ""
    tags: ClassVar[tuple[str, ...]] = ()
    full_path: ClassVar[str] = ""
    Body: ClassVar[type[BaseModel]]
    Response: ClassVar[type[BaseModel]]
    Query: ClassVar[type[BaseModel]]

    @classmethod
    def path_params(cls) -> list[str]:
        return [m.group("name") for m in _PATH_PARAM_RE.finditer(cls.path)]

    @classmethod
    def url(cls, **params: Any) -> str:
        required = cls.path_params()
        missing = [p for p in required if p not in params]
        if missing:
            raise KeyError(f"{cls._label()}: missing path parameter(s) {missing}")

        def repl(match: re.Match[str]) -> str:
            return str(params[match.group("name")])

        return _PATH_PARAM_RE.sub(repl, cls.path)

    @classmethod
    def parse_body(cls, data: Any) -> BaseModel:
        if not hasattr(cls, "Body"):
            raise ValueError(f"{cls._label()}: no Body type defined")
        return cls.Body.model_validate(data)

    @classmethod
    def parse_response(cls, data: Any) -> BaseModel:
        if not hasattr(cls, "Response"):
            raise ValueError(f"{cls._label()}: no Response type defined")
        return cls.Response.model_validate(data)

    @classmethod
    def parse_query(cls, data: Any) -> BaseModel:
        if not hasattr(cls, "Query"):
            raise ValueError(f"{cls._label()}: no Query type defined")
        return cls.Query.model_validate(data)

    @classmethod
    def _label(cls) -> str:
        return cls.name or f"{cls.method.value} {cls.path}"


@dataclass
class EndpointGroup:
    prefix: str = ""
    tags: tuple[str, ...] = ()
    endpoints: list[type[Endpoint]] = field(default_factory=list)

    def add(self, endpoint: type[Endpoint]) -> type[Endpoint]:
        if self.prefix:
            sub = endpoint.path.lstrip("/")
            endpoint.full_path = self.prefix.rstrip("/") + ("/" + sub if sub else "")
        else:
            endpoint.full_path = endpoint.path
        if not endpoint.tags:
            endpoint.tags = self.tags
        self.endpoints.append(endpoint)
        return endpoint

    def __iter__(self) -> Iterator[type[Endpoint]]:
        return iter(self.endpoints)

    def __len__(self) -> int:
        return len(self.endpoints)
