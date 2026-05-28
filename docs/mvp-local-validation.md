# MVP local validation

This document records the first successful local validation of the Tactical NetDevOps Validator MVP.

## 1. Environment

The project was executed locally from a Python virtual environment.

The installed command-line entry point was:

```bash
tactical-validator
```

## 2. Unit tests

Command executed:

```bash
pytest -q
```

Observed result:

```text
........                                                                                                                       [100%]
8 passed in 0.07s
```

Interpretation:

The parser and evaluator tests passed successfully.

## 3. Nominal scenario

Command executed:

```bash
tactical-validator validate --scenario examples/outputs/nominal --output reports/nominal-report.json --html reports/nominal-report.html
```

Observed result:

```text
GREEN / NOMINAL: Network is operating in nominal state using the primary path via HELI-ALFA.
```

Interpretation:

The validator correctly detected that the primary path is active:

```text
BASE -> HELI-ALFA -> HELI-BRAVO
```

## 4. Degraded scenario

Command executed:

```bash
tactical-validator validate --scenario examples/outputs/degraded --output reports/degraded-report.json --html reports/degraded-report.html
```

Observed result:

```text
YELLOW / DEGRADED: Network is degraded: backup path via HELI-CHARLIE is in use.
```

Interpretation:

The validator correctly detected that the network is still reachable, but using the backup path:

```text
BASE -> HELI-CHARLIE -> HELI-BRAVO
```

## 5. ECMP scenario

Command executed:

```bash
tactical-validator validate --scenario examples/outputs/ecmp --output reports/ecmp-report.json --html reports/ecmp-report.html
```

Observed result:

```text
INFO / ECMP_DETECTED: ECMP detected: OSPF has installed both primary and backup next-hops.
```

Interpretation:

The validator correctly detected that OSPF installed both the primary and backup next-hops as equal-cost paths.

This is not treated as a critical failure, but as an informational state because the network still has valid paths while the result may not be deterministic for a primary/backup demonstration.

## 6. Critical scenario

Command executed:

```bash
tactical-validator validate --scenario examples/outputs/critical --output reports/critical-report.json --html reports/critical-report.html
```

Observed result:

```text
RED / CRITICAL: Network is critical: no valid route to HELI-BRAVO loopback.
```

Interpretation:

The validator correctly detected that there is no valid route towards the target loopback:

```text
HELI-BRAVO loopback: 192.168.3.1/32
```

This represents a critical operational state because the destination node is not reachable through either the primary or backup path.

## 7. Result

The MVP is functional.

The tool can parse saved Cisco IOS command outputs, evaluate the operational state of the OSPF resilience lab and generate JSON/HTML reports for the four target states:

- `GREEN / NOMINAL`
- `YELLOW / DEGRADED`
- `RED / CRITICAL`
- `INFO / ECMP_DETECTED`

## 8. Next step

Add the generated JSON and HTML reports to the repository as sample outputs:

```text
reports/nominal-report.json
reports/nominal-report.html
reports/degraded-report.json
reports/degraded-report.html
reports/ecmp-report.json
reports/ecmp-report.html
reports/critical-report.json
reports/critical-report.html
```

These reports can be referenced from the README and used as visual evidence for the project portfolio.
