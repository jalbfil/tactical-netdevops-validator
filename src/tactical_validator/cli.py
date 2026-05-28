from __future__ import annotations
import argparse
from pathlib import Path
from tactical_validator.collector import collect_from_device
from tactical_validator.evaluator import evaluate_network_state
from tactical_validator.inventory import load_inventory
from tactical_validator.parsers import parse_ip_route, parse_ospf_neighbors, parse_traceroute
from tactical_validator.reporter import write_html_report, write_json_report
DEFAULT_OSPF_FILE='base_show_ip_ospf_neighbor.txt'; DEFAULT_ROUTE_FILE='base_show_ip_route_bravo.txt'; DEFAULT_TRACEROUTE_FILE='base_traceroute_bravo.txt'
def _read_optional(path: Path) -> str: return path.read_text(encoding='utf-8') if path.exists() else ''
def validate_offline(args):
    scenario=Path(args.scenario); neighbors=parse_ospf_neighbors(_read_optional(scenario/DEFAULT_OSPF_FILE)); route=parse_ip_route(_read_optional(scenario/DEFAULT_ROUTE_FILE), target=args.target); tout=_read_optional(scenario/DEFAULT_TRACEROUTE_FILE); tr=parse_traceroute(tout, target=args.target) if tout else None
    report=evaluate_network_state(neighbors, route, tr); write_json_report(report,args.output)
    if args.html: write_html_report(report,args.html)
    print(f"{report.status.value} / {report.state.value}: {report.summary}")
def validate_live(args):
    devices=load_inventory(args.inventory); base=next((d for d in devices if d.name.upper()=='BASE'),None)
    if not base: raise RuntimeError('Inventory must include a device named BASE')
    ev=collect_from_device(base); report=evaluate_network_state(parse_ospf_neighbors(ev.outputs['ospf_neighbors']), parse_ip_route(ev.outputs['route_to_bravo'], target=args.target), parse_traceroute(ev.outputs['traceroute_to_bravo'], target=args.target))
    write_json_report(report,args.output)
    if args.html: write_html_report(report,args.html)
    print(f"{report.status.value} / {report.state.value}: {report.summary}")
def build_parser():
    p=argparse.ArgumentParser(prog='tactical-validator', description='Validate tactical OSPF lab state from command outputs or live SSH collection.'); sp=p.add_subparsers(dest='command', required=True)
    off=sp.add_parser('validate', help='Validate from saved command outputs'); off.add_argument('--scenario', required=True); off.add_argument('--target', default='192.168.3.1'); off.add_argument('--output', default='reports/report.json'); off.add_argument('--html'); off.set_defaults(func=validate_offline)
    live=sp.add_parser('validate-live', help='Validate by collecting evidence via SSH'); live.add_argument('--inventory', required=True); live.add_argument('--target', default='192.168.3.1'); live.add_argument('--output', default='reports/live-report.json'); live.add_argument('--html'); live.set_defaults(func=validate_live)
    return p
def main():
    args=build_parser().parse_args(); args.func(args)
