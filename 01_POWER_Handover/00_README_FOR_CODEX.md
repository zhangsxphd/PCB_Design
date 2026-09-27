# PBC_Design Handover - Irrigation-C3 Mainboard V1 (01_POWER)

## Status Update for Codex
The exported `01_POWER` artifacts are internally consistent with the Version 1.2 netlist baseline. The local verification script checks the two exports against each other, verifies the golden netlist and nominal feedback-divider math, and confirms that U1 EN is the only intentionally unconnected pin.

This is **not** a PCB-release sign-off. The check does not prove live EasyEDA save state, ERC/DRC status, component derating, transient behavior, or PCB layout. The rendered schematic also needs a readability cleanup before it should be treated as a maintained design document; several labels and long wire paths overlap or obscure the circuit flow.

## Handover Files

* `01_01_POWER_Connectivity.json`: The layout-independent graph IR representing the pure electrical connections. This is the single source of truth for the Golden Netlist.
* `01_02_POWER_Components.json`: The complete list of components with their definitive properties, footprints, and exact LCSC bindings. R1 (100kΩ) and R3 (45.3kΩ) have been forced to exact part numbers to fix buck outputs (5.08V and 3.318V respectively).
* `01_03_POWER_Verification_Script.py`: Reproducible local consistency checks. It reads the two files above using paths relative to the script, checks unmarked floating pins, anonymous/duplicate nets, component identities, exact node-to-node matching, provisional fuse exclusions, and nominal divider math.
* `01_04_PCB_RELEASE_BLOCKERS.md`: Pending physical-world tasks (Fuses, TVS sizing) that must be resolved prior to PCB layout.
* `01_05_POWER_Schematic.pdf` / `01_06_POWER_Schematic.svg`: High-resolution visual snapshots of the exported schematic baseline.

## Architecture Snapshot
* **Input**: 12V_IN via J1 -> F1 -> D1 -> 12V_PROTECTED.
* **Buck 1**: TPS54302 drops 12V_PROTECTED to 5.08V (BUCK_5V). EN is intentionally NC (internal pull-up).
* **Branches**:
  - `BUCK_5V` routes directly to `SCALE_5V` via F3.
  - `12V_PROTECTED` routes directly to `PUMP_FUSE_OUT` via F2.
* **Logic/MCU Power**: `LOGIC_5V` is diode-OR'd (D3, D4) from `BUCK_5V` and `USB_5V` (to be created on page 02).
* **Buck 2**: TLV62569 drops `LOGIC_5V` to exactly 3.318V (`3V3`).

## Next Action Required
Resolve the release blockers and clean up the schematic layout in a connected EasyEDA session before importing this page into PCB. Do not modify the live `01_POWER_CLEAN` document without explicit user permission and a successful typed `easyeda health` connection.
