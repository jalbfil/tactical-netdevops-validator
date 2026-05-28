from __future__ import annotations

import re

from tactical_validator.models import RouteInfo


ROUTE_HEADER_RE = re.compile(
    r'Known via "(?P<protocol>[^\"]+)", distance (?P<distance>\d+), metric (?P<metric>\d+)'
)
NEXT_HOP_RE = re.compile(r"\*?\s*(?P<next_hop>\d+\.\d+\.\d+\.\d+),\s+from\s+")


def parse_ip_route(output: str, target: str = "192.168.3.1") -> RouteInfo:
    """Parse Cisco IOS `show ip route <target>` output."""
    if not output.strip() or "not in table" in output.lower() or "subnet not in table" in output.lower():
        return RouteInfo(target=target, exists=False, raw=output)

    if "Routing entry for" not in output:
        return RouteInfo(target=target, exists=False, raw=output)

    protocol: str | None = None
    distance: int | None = None
    metric: int | None = None

    header = ROUTE_HEADER_RE.search(output)
    if header:
        protocol = header.group("protocol")
        distance = int(header.group("distance"))
        metric = int(header.group("metric"))

    next_hops: list[str] = []
    for match in NEXT_HOP_RE.finditer(output):
        next_hop = match.group("next_hop")
        if next_hop not in next_hops:
            next_hops.append(next_hop)

    return RouteInfo(
        target=target,
        exists=True,
        protocol=protocol,
        distance=distance,
        metric=metric,
        next_hops=next_hops,
        raw=output,
    )
