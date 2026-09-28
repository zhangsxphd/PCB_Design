# Design baseline

## A. User's ESP32-C3 SuperMini compatibility reference

The task text describes a working ESP32-C3FN4 SuperMini prototype with native Type-C USB, a GPIO8 board LED, UART-related GPIO20/21 and a board-specific warning against simultaneous external/USB power. These are compatibility facts from the user's reference, not a circuit to copy. The custom board uses the Page-01 diode-OR power path and reserves GPIO8 as a strap.

## B. Official/manufacturer design basis

- [Espressif ESP32-C3-MINI-1 datasheet](https://documentation.espressif.com/esp32-c3-mini-1_datasheet_en.html): module pin map, integrated flash/crystal/RF/antenna; all official GND pads and NC pins were checked against the live library.
- [Espressif ESP32-C3 hardware design checklist](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/schematic-checklist.html): GPIO18 D−, GPIO19 D+, GPIO20 U0RXD, GPIO21 U0TXD; GPIO2/8/9 straps; EN pull-up/RC, USB resistor and tuning footprints, ADC input filter and USB layout guidance.
- [ST USBLC6-2SC6 datasheet](https://www.st.com/resource/en/datasheet/usblc6-2.pdf): U4 I/O1 pins 1/6, I/O2 pins 3/4, GND pin 2 and VBUS pin 5.
- [XKB U262-161N-4BVC11 manufacturer drawing](https://atta.szlcsc.com/upload/public/pdf/source/20260728/068D23378A0F298149652B95EF784648.pdf): J2 contact functions were compared with the actual EasyEDA symbol pins.

Firmware must explicitly select `SDA=GPIO0` and `SCL=GPIO1` (for example `Wire.begin(0, 1)`); do not rely on an Arduino board default. Native USB is the programming/debug path. GPIO4/5 remain SCALE_RX/TX, and GPIO20/21 remain expansion UART RX/TX.

PCB follow-up: target USB D+/D− differential impedance 90 Ω ±10%, matched pair with continuous ground return, minimal vias/stubs and pump/switching separation. Put U4 at J2, R7/R8 and DNP C13/C14 near U3. Keep U3 antenna at the carrier edge with all-layer copper/trace/component clearance; no RF matching circuit was added. Place C10/C11 near U3 3V3. These are layout requirements, not completed PCB work.
