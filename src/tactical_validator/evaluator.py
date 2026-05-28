from __future__ import annotations
from tactical_validator.models import CheckResult, NetworkState, OspfNeighbor, RouteInfo, Status, TracerouteInfo, ValidationReport, utc_now_iso
PRIMARY_NEXT_HOP = "10.0.1.2"; BACKUP_NEXT_HOP = "10.0.4.2"; ALFA_ROUTER_ID = "2.2.2.2"; CHARLIE_ROUTER_ID = "4.4.4.4"; TARGET_NODE = "HELI-BRAVO"; TARGET_LOOPBACK = "192.168.3.1"
def _neighbor_state(neighbors: list[OspfNeighbor], router_id: str) -> OspfNeighbor | None: return next((n for n in neighbors if n.router_id == router_id), None)
def _neighbor_dict(n: OspfNeighbor) -> dict[str, str | bool | None]:
    node_map = {ALFA_ROUTER_ID: "HELI-ALFA", CHARLIE_ROUTER_ID: "HELI-CHARLIE", "3.3.3.3": "HELI-BRAVO"}
    return {"router_id": n.router_id, "node": node_map.get(n.router_id, "UNKNOWN"), "state": n.state, "address": n.address, "interface": n.interface, "is_full": n.is_full}
def evaluate_network_state(neighbors: list[OspfNeighbor], route: RouteInfo, traceroute: TracerouteInfo | None = None) -> ValidationReport:
    checks: list[CheckResult] = []
    alfa = _neighbor_state(neighbors, ALFA_ROUTER_ID); charlie = _neighbor_state(neighbors, CHARLIE_ROUTER_ID)
    alfa_full = bool(alfa and alfa.is_full); charlie_full = bool(charlie and charlie.is_full)
    checks.append(CheckResult("route_to_target", "PASS" if route.exists else "FAIL", "Route to target exists" if route.exists else "No route to target"))
    checks.append(CheckResult("ospf_neighbor_alfa", "PASS" if alfa_full else "WARN", "HELI-ALFA OSPF adjacency is FULL" if alfa_full else "HELI-ALFA OSPF adjacency is not FULL/available"))
    checks.append(CheckResult("ospf_neighbor_charlie", "PASS" if charlie_full else "WARN", "HELI-CHARLIE OSPF adjacency is FULL" if charlie_full else "HELI-CHARLIE OSPF adjacency is not FULL/available"))
    if traceroute: checks.append(CheckResult("traceroute_to_target", "PASS" if traceroute.success else "WARN", f"Traceroute hops: {' -> '.join(traceroute.hops)}" if traceroute.hops else "Traceroute did not return usable hops"))
    target={"node": TARGET_NODE, "loopback": TARGET_LOOPBACK}; ospf=[_neighbor_dict(n) for n in neighbors]
    if not route.exists: return ValidationReport("tactical-netdevops-validator", utc_now_iso(), Status.RED, NetworkState.CRITICAL, target, None, [], ospf, checks, "Network is critical: no valid route to HELI-BRAVO loopback.")
    next_hops=list(dict.fromkeys(route.next_hops)); has_primary=PRIMARY_NEXT_HOP in next_hops; has_backup=BACKUP_NEXT_HOP in next_hops
    if len(next_hops)>1 and has_primary and has_backup: return ValidationReport("tactical-netdevops-validator", utc_now_iso(), Status.INFO, NetworkState.ECMP_DETECTED, target, None, next_hops, ospf, checks+[CheckResult("ecmp_detected", "INFO", "Multiple equal-cost paths detected towards HELI-BRAVO")], "ECMP detected: OSPF has installed both primary and backup next-hops.")
    if has_primary: return ValidationReport("tactical-netdevops-validator", utc_now_iso(), Status.GREEN, NetworkState.NOMINAL, target, ["BASE","HELI-ALFA","HELI-BRAVO"], next_hops, ospf, checks, "Network is operating in nominal state using the primary path via HELI-ALFA.")
    if has_backup: return ValidationReport("tactical-netdevops-validator", utc_now_iso(), Status.YELLOW, NetworkState.DEGRADED, target, ["BASE","HELI-CHARLIE","HELI-BRAVO"], next_hops, ospf, checks+[CheckResult("backup_path_in_use", "WARN", "Backup path is active; primary path is not currently used")], "Network is degraded: backup path via HELI-CHARLIE is in use.")
    return ValidationReport("tactical-netdevops-validator", utc_now_iso(), Status.RED, NetworkState.CRITICAL, target, None, next_hops, ospf, checks+[CheckResult("unknown_next_hop", "FAIL", f"Unexpected next-hop(s): {', '.join(next_hops)}")], "Network is critical or unknown: route exists but next-hop is not part of the expected topology.")
