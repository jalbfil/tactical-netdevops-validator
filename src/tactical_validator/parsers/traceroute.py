from __future__ import annotations

import re

from tactical_validator.models import TracerouteInfo


HOP_RE = re.compile(r"^\s*\d+\s+(?P<hop>\d+\.\d+\.\d+\.\d+)\s+")


def parse_traceroute(output: str, target: str = "192.168.3.1") -> TracerouteInfo:
    """Parse a simple Cisco IOS traceroute output and return hop IPs."""
    hops: list[str] = []

    for raw_line in output.splitlines():
        match = HOP_RE.match(raw_line)
        if not match:
            continue
        hops.append(match.group("hop"))

    return TracerouteInfo(target=target, hops=hops, raw=output)
