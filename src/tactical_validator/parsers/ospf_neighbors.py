from __future__ import annotations

import re

from tactical_validator.models import OspfNeighbor


NEIGHBOR_RE = re.compile(
    r"^(?P<router_id>\d+\.\d+\.\d+\.\d+)\s+"
    r"(?P<priority>\d+)\s+"
    r"(?P<state>\S+)\s+"
    r"(?P<dead_time>\S+)\s+"
    r"(?P<address>\d+\.\d+\.\d+\.\d+)\s+"
    r"(?P<interface>\S+)"
)


def parse_ospf_neighbors(output: str) -> list[OspfNeighbor]:
    """Parse Cisco IOS `show ip ospf neighbor` output."""
    neighbors: list[OspfNeighbor] = []

    for raw_line in output.splitlines():
        line = raw_line.strip()
        match = NEIGHBOR_RE.match(line)
        if not match:
            continue
        neighbors.append(
            OspfNeighbor(
                router_id=match.group("router_id"),
                state=match.group("state"),
                address=match.group("address"),
                interface=match.group("interface"),
            )
        )

    return neighbors
