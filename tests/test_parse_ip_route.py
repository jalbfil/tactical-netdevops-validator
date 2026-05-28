from pathlib import Path
from tactical_validator.parsers import parse_ip_route

def test_parse_nominal_route():
    output = Path("examples/outputs/nominal/base_show_ip_route_bravo.txt").read_text()
    route = parse_ip_route(output)
    assert route.exists
    assert route.next_hops == ["10.0.1.2"]
    assert route.metric == 21

def test_parse_ecmp_route():
    output = Path("examples/outputs/ecmp/base_show_ip_route_bravo.txt").read_text()
    route = parse_ip_route(output)
    assert route.exists
    assert set(route.next_hops) == {"10.0.1.2", "10.0.4.2"}
    assert route.has_ecmp

def test_parse_missing_route():
    output = Path("examples/outputs/critical/base_show_ip_route_bravo.txt").read_text()
    route = parse_ip_route(output)
    assert not route.exists
