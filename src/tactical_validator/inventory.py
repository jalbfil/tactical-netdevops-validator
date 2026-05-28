from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import yaml
@dataclass(frozen=True)
class Device:
    name: str; host: str; device_type: str = "cisco_ios"; username: str | None = None; password: str | None = None
def load_inventory(path: str | Path) -> list[Device]:
    data=yaml.safe_load(Path(path).read_text(encoding='utf-8'))
    return [Device(name=i['name'], host=i['host'], device_type=i.get('device_type','cisco_ios'), username=i.get('username'), password=i.get('password')) for i in data.get('devices',[])]
