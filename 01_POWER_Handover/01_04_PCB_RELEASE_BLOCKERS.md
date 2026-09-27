# 01_POWER PCB Release Blockers

The following components are currently acting as placeholders and MUST be finalized before PCB Layout routing begins:

1. **F1, F2, F3 (Fuses / PTC) - hard blocker**
   - Currently marked as `TBD_MEASURE` and excluded from BOM/PCB (`addIntoBom: false`, `addIntoPcb: false`).
   - Action Required: Determine exact trip current and footprint based on final pump/valve/sensor load profiling.

2. **D1 reverse-polarity protection - hard blocker**
   - The snapshot currently binds SS34 / C8678 and includes it in BOM/PCB; it is therefore not a placeholder in the exported data.
   - Confirm the continuous and surge current after the pump/valve load profile is known. At 3 A the listed 550 mV forward drop implies up to 1.65 W in the series diode, so thermal loss and voltage headroom must be reviewed. Consider an appropriately rated ideal-diode MOSFET solution if efficiency or drop is unacceptable.

3. **D2 input TVS - hard blocker**
   - The snapshot currently binds SMAJ15A / C143119 and includes it in BOM/PCB.
   - Confirm maximum normal input voltage, source impedance, cable/inductive transient class, required surge waveform/energy, and fuse coordination before accepting the 15 V standoff / 24.4 V maximum clamp selection.

4. **Loads, connectors, and power budget - hard blocker**
   - Record maximum/steady current for the pump branch, scale branch, BUCK_5V rail, USB backfeed case, and 3V3 rail.
   - Confirm J1, traces, copper temperature rise, diode-OR losses, and both converters against those loads and ambient temperature.

5. **Schematic maintainability - must fix before release**
   - Re-layout the live schematic so the power flow is left-to-right, local connections use short visible wires, and net labels do not overlap symbols, values, or the title block.
   - Re-run typed save -> reload -> fresh dump/check after the cleanup. The exported PDF is evidence of connectivity, not evidence of acceptable schematic readability.

DO NOT import `01_POWER` into PCB until these blockers are resolved. Re-enable F1/F2/F3 only after final parts and footprints are bound; replace or explicitly approve D1/D2 before release.
