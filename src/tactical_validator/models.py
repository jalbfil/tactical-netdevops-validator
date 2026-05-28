from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class Status(str, Enum):
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    RED = "RED"
    INFO = "INFO"


class NetworkState(str, Enum):
    NOMINAL = "NOMINAL"
    DEGRADED = "DEGRADED"
    CRITICAL = "CRITICAL"
    ECMP_DETECTED = "ECMP_DETECTED"


@dataclass(frozen=True)
class OspfNeighbor:
    router_id: str
    state: str
    address: str
    interface: str

    @property
    def is_full(self) -> bool:
        return self.state.upper().startswith("FULL")


@dataclass(frozen=True)
class RouteInfo:
    target: str
    exists: bool
    protocol: str | None = None
    distance: int | None = None
    metric: int | None = None
    next_hops: list[str] = field(default_factory=list)
    raw: str = ""

    @property
    def has_ecmp(self) -> bool:
        return len(set(self.next_hops)) > 1

    def has_next_hop(self, next_hop: str) -> bool:
        return next_hop in self.next_hops


@dataclass(frozen=True)
class TracerouteInfo:
    target: str
    hops: list[str] = field(default_factory=list)
    raw: str = ""

    @property
    def success(self) -> bool:
        return bool(self.hops)


@dataclass(frozen=True)
class CheckResult:
    name: str
    result: str
    detail: str

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "result": self.result, "detail": self.detail}


@dataclass(frozen=True)
class ValidationReport:
    validator: str
    timestamp: str
    status: Status
    state: NetworkState
    target: dict[str, str]
    active_path: list[str] | None
    next_hops: list[str]
    ospf_neighbors: list[dict[str, Any]]
    checks: list[CheckResult]
    summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "validator": self.validator,
            "timestamp": self.timestamp,
            "status": self.status.value,
            "state": self.state.value,
            "target": self.target,
            "active_path": self.active_path,
            "next_hops": self.next_hops,
            "ospf_neighbors": self.ospf_neighbors,
            "checks": [check.to_dict() for check in self.checks],
            "summary": self.summary,
        }
