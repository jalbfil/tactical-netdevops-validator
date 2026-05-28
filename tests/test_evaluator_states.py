from pathlib import Path
from tactical_validator.evaluator import evaluate_network_state
from tactical_validator.models import NetworkState, Status
from tactical_validator.parsers import parse_ip_route, parse_ospf_neighbors, parse_traceroute

def load_report(scenario: str):
    base = Path("examples/outputs") / scenario
    neighbors = parse_ospf_neighbors((base / "base_show_ip_ospf_neighbor.txt").read_text())
    route = parse_ip_route((base / "base_show_ip_route_bravo.txt").read_text())
    traceroute = parse_traceroute((base / "base_traceroute_bravo.txt").read_text())
    return evaluate_network_state(neighbors, route, traceroute)

def test_nominal_state():
    report = load_report("nominal")
    assert report.status == Status.GREEN
    assert report.state == NetworkState.NOMINAL
    assert report.active_path == ["BASE", "HELI-ALFA", "HELI-BRAVO"]

def test_degraded_state():
    report = load_report("degraded")
    assert report.status == Status.YELLOW
    assert report.state == NetworkState.DEGRADED
    assert report.active_path == ["BASE", "HELI-CHARLIE", "HELI-BRAVO"]

def test_critical_state():
    report = load_report("critical")
    assert report.status == Status.RED
    assert report.state == NetworkState.CRITICAL
    assert report.active_path is None

def test_ecmp_state():
    report = load_report("ecmp")
    assert report.status == Status.INFO
    assert report.state == NetworkState.ECMP_DETECTED
    assert set(report.next_hops) == {"10.0.1.2", "10.0.4.2"}
