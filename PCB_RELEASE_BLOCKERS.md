# PCB release blockers

PCB release is intentionally blocked. Do not create or update PCB from this handover yet.

1. F1/F2/F3 are deliberate placeholders: measure/procure exact fuse part numbers, footprints, current ratings and interrupt ratings.
2. Confirm C9 voltage, ripple-current, temperature-life and polarity against the selected manufacturer datasheet.
3. Obtain manufacturer DC-bias/derating evidence for the MLCCs before finalizing effective capacitance.
4. Confirm L1/L2 saturation/current/thermal margins in the final enclosure and switching-frequency conditions.
5. Resolve remaining EasyEDA visual marker/cluster diagnostics before claiming schematic release completeness.

`02_ESP32_USB` and all PCB work are out of scope for this release.
