# Page 02 final review

Project: `Irrigation-C3_Mainboard_V1` · Page: `02_ESP32_USB` · saved and reloaded on 2026-09-28.

**Electrical snapshot verification: PASS. Schematic release: FAIL. PCB release: BLOCKED.**

The live page contains 30 real EasyEDA library parts, 28 named nets and 113 pin connections. The read-only `02_03_ESP32_USB_Verification.py` checks the full saved Golden Netlist, frozen U3/J2/U4 identities, all U3 GND pads, exact U3/J2 NC sets, GPIO assignments, USB polarity/ESD/CC/VBUS, EN/BOOT/strap circuits, PUMP_EN pull-down, DNP tuning/pull-ups and excluded ADC divider placeholders. `scripts/verify_all.py` passes both Page-01 and Page-02 electrical snapshots. The native bridge check reports zero bridges and zero orphans.

| Gate | Saved-state result |
| --- | --- |
| Component overlaps / out of sheet | 0 / 0 (`02_13_LIVE_LAYOUT_LINT.json`) |
| Floating pins / geometry net mismatch / marker mismatch / multi-net wires | 0 / 0 / 0 / 0 (`02_12_LIVE_SCH_CHECK.json`) |
| Wire over pin / zero-length / dangling / title-block overlap / marker overlap | 0 / 0 / 0 / 0 / 0 |
| Strict cluster ERROR | 0; 16 spacing WARN (`02_14_LIVE_CLUSTERS_STRICT.json`) |
| Bridge / orphan | 0 / 0 (`02_11_LIVE_BRIDGE_CHECK.json`) |
| Native DRC fatal / error / warning | 0 / 0 / **30 aggregate, unitemized** (`02_17_LIVE_DRC.json`) |
| Functional partition check | **1 missing-partition finding**; planned six-zone frames overlap in seven places |
| Independent wire-through-body audit | Not established by the current checker; no release claim made |

The exported schematic visibly needs layout refinement, especially text around U3/J2/U4 and the ADC branch. The six-zone `sch zone-plan` cannot draw non-overlapping frames around the present positions (`zone-plan.json` retained in ignored local work evidence); no overlapping frame was committed as a cosmetic fix. The typed schematic API used here also has no supported independent note-creation action, so the requested USB/antenna/decoupling notes are documented in `REFERENCE_BASELINE.md` but are not visible annotations on the page. The native DRC API provides only an aggregate warning count, so `02_DRC_WAIVERS.json` contains no invented waivers. These gates prevent `SCHEMATIC_RELEASE=PASS`, even though the electrical snapshot passes. The `sch check` also reports nine verified, non-junction wire crossings as information rather than shorts.

R18/R19 are schematic placeholders with `Value=TBD_CALC`, `STATUS=WAIT_INPUT_MAX`, `DO_NOT_RELEASE_TO_PCB=TRUE`, `addIntoBom=false` and `addIntoPcb=false`. Their placed library symbol comes from a real 10 kΩ component, but that stock value is **not** the selected divider value. SW1/SW2 and LED1/LED2 are provisional production selections; C13/C14 and R16/R17 default to DNP. The remaining PCB blockers are recorded in `02_04_PCB_RELEASE_BLOCKERS.md`.

The canonical `.epro2` is an official export of the saved live project. Comparison of the native archive's document sections found the original Page-01 and other pre-existing document sections unchanged; only Page 02 and the required library sections were added/changed. No PCB document was edited and Pages 03–05 were not developed.
