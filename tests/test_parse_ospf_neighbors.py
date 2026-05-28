from pathlib import Path
from tactical_validator.parsers import parse_ospf_neighbors

def test_parse_ospf_neighbors_nominal():
    output = Path("examples/outputs/nominal/base_show_ip_ospf_neighbor.txt").read_text()
    neighbors = parse_ospf_neighbors(output)
    assert len(neighbors) == 2
    assert neighbors[0].router_id == "2.2.2.2"
    assert neighbors[0].is_full
    assert neighbors[1].router_id == "4.4.4.4"
