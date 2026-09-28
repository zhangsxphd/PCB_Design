# Page 02 PCB release blockers

PCB release remains **BLOCKED**. No Page-02 PCB synchronization or layout was done.

| ID | Open item |
| --- | --- |
| BLOCKER-02-001 | Resolve `12V_INPUT_MAX_ALLOWED`, then calculate and validate R18/R19; both are `TBD_CALC` and excluded from BOM/PCB. |
| BLOCKER-02-002 | Verify 3V3 Wi-Fi peak current and TLV62569 margin using final load and thermal conditions. |
| BLOCKER-02-003 | Establish stack-up and verify 90 Ω ±10% USB differential impedance and matched D+/D− routing. |
| BLOCKER-02-004 | Place U3 antenna at the board edge and enforce all-layer copper, trace and component keepout. |
| BLOCKER-02-005 | Confirm J2 edge placement and mechanical/enclosure fit. |
| BLOCKER-02-006 | Place U4 close to J2 with a short ESD return path. |
| BLOCKER-02-007 | Keep C13/C14 DNP until USB hardware tuning confirms whether they are needed. |
| BLOCKER-02-008 | Freeze exact production switch parts SW1/SW2. |
| BLOCKER-02-009 | Freeze exact production LED parts LED1/LED2 and optical/current requirements. |
| BLOCKER-02-010 | Review full 3V3 decoupling, power return and USB/pump current separation in layout. |

Schematic release is also pending clean functional partition geometry, visual cleanup and attribution of 30 aggregate native DRC warnings. See `02_16_FINAL_RELEASE_REPORT.md`.
