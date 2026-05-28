from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv
from netmiko import ConnectHandler
from tactical_validator.inventory import Device
COMMANDS={"ospf_neighbors":"show ip ospf neighbor","route_to_bravo":"show ip route 192.168.3.1","traceroute_to_bravo":"traceroute 192.168.3.1"}
@dataclass(frozen=True)
class CollectedEvidence:
    device_name: str; outputs: dict[str,str]
def collect_from_device(device: Device) -> CollectedEvidence:
    load_dotenv(); username=device.username or os.getenv('ROUTER_USERNAME'); password=device.password or os.getenv('ROUTER_PASSWORD')
    if not username or not password: raise RuntimeError('Missing credentials. Set ROUTER_USERNAME and ROUTER_PASSWORD or define them in inventory.')
    params={"device_type":device.device_type,"host":device.host,"username":username,"password":password,"fast_cli":False}; outputs={}
    with ConnectHandler(**params) as conn:
        for k,cmd in COMMANDS.items(): outputs[k]=conn.send_command(cmd, read_timeout=30)
    return CollectedEvidence(device.name, outputs)
