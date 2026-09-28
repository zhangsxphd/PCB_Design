# 02_ESP32_USB handover

The page is drawn in the live EasyEDA Pro project and exported into the single canonical `easyeda_source/Irrigation-C3_Mainboard_V1.epro2`. Electrical verification passes; **schematic release is still FAIL** because functional partition frames are missing and the native DRC returns 30 unitemized warnings. PCB release remains BLOCKED.

Run `python3 scripts/verify_all.py` from the repository root. This verifies the frozen Page-01 and Page-02 electrical snapshots without writing to EasyEDA. `02_03_ESP32_USB_Verification.py` can be run alone. The `02_08`–`02_14` JSON files are live saved-and-reloaded readbacks; `02_05`–`02_07` are direct EasyEDA page exports. `02_16_FINAL_RELEASE_REPORT.md` describes the release limitations. `REFERENCE_BASELINE.md` separates the user's SuperMini reference from official module/manufacturer design rules.

Native DRC warning identities were unavailable from the connector. `02_DRC_WAIVERS.json` therefore makes no waiver claim. Do not use these outputs to release a PCB or a production BOM.
