# Validation logic

Target: `192.168.3.1/32` (`HELI-BRAVO`).

| Path | Next-hop | Meaning |
|---|---:|---|
| Primary | `10.0.1.2` | BASE -> HELI-ALFA |
| Backup | `10.0.4.2` | BASE -> HELI-CHARLIE |

- `GREEN`: route uses `10.0.1.2`.
- `YELLOW`: route uses `10.0.4.2`.
- `RED`: no route or unknown next-hop.
- `INFO`: both next-hops are installed as ECMP.
