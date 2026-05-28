from __future__ import annotations
import html, json
from pathlib import Path
from tactical_validator.models import ValidationReport

def write_json_report(report: ValidationReport, output_path: str | Path) -> None:
    path=Path(output_path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(report.to_dict(), indent=2), encoding='utf-8')

def write_html_report(report: ValidationReport, output_path: str | Path) -> None:
    data=report.to_dict(); status=html.escape(data['status']); state=html.escape(data['state']); summary=html.escape(data['summary'])
    next_hops=', '.join(html.escape(h) for h in data['next_hops']) or 'N/A'
    active_path=' -> '.join(data['active_path']) if data['active_path'] else 'N/A'
    checks='\n'.join(f"<tr><td>{html.escape(c['name'])}</td><td>{html.escape(c['result'])}</td><td>{html.escape(c['detail'])}</td></tr>" for c in data['checks'])
    neigh='\n'.join('<tr>'+f"<td>{html.escape(str(n.get('node')))}</td><td>{html.escape(str(n.get('router_id')))}</td><td>{html.escape(str(n.get('state')))}</td><td>{html.escape(str(n.get('address')))}</td><td>{html.escape(str(n.get('interface')))}</td>"+'</tr>' for n in data['ospf_neighbors'])
    doc=f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Tactical NetDevOps Validator Report</title><style>body{{font-family:Arial,sans-serif;margin:32px;background:#f6f8fa;color:#24292f}}.card{{background:#fff;border:1px solid #d0d7de;border-radius:8px;padding:20px;margin-bottom:18px}}.status{{font-size:28px;font-weight:bold}}table{{width:100%;border-collapse:collapse;margin-top:12px}}th,td{{border:1px solid #d0d7de;padding:8px;text-align:left}}th{{background:#f0f3f6}}code{{background:#f0f3f6;padding:2px 4px;border-radius:4px}}</style></head><body><div class='card'><div class='status'>Status: {status} / {state}</div><p>{summary}</p><p><strong>Target:</strong> {html.escape(data['target']['node'])} — <code>{html.escape(data['target']['loopback'])}</code></p><p><strong>Active path:</strong> {html.escape(active_path)}</p><p><strong>Next-hop(s):</strong> <code>{next_hops}</code></p><p><strong>Timestamp:</strong> {html.escape(data['timestamp'])}</p></div><div class='card'><h2>OSPF neighbors</h2><table><tr><th>Node</th><th>Router ID</th><th>State</th><th>Address</th><th>Interface</th></tr>{neigh}</table></div><div class='card'><h2>Checks</h2><table><tr><th>Check</th><th>Result</th><th>Detail</th></tr>{checks}</table></div></body></html>"""
    path=Path(output_path); path.parent.mkdir(parents=True,exist_ok=True); path.write_text(doc,encoding='utf-8')
