#!/usr/bin/env python3
"""Reproducible consistency checks for the 01_POWER handover artifacts.

This validates the exported connectivity and component snapshots. It does not
replace an EasyEDA ERC/DRC run or prove that the live document was saved.
"""

import json
import math
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CONNECTIVITY_PATH = BASE_DIR / "01_01_POWER_Connectivity.json"
COMPONENTS_PATH = BASE_DIR / "01_02_POWER_Components.json"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def component_value(component):
    return component.get("otherProperty", {}).get("Value", component.get("name", ""))


def verify_voltage(r_top, r_bottom, v_ref, expected_v, name):
    actual_v = v_ref * (1 + r_top / r_bottom)
    require(math.isclose(actual_v, expected_v, abs_tol=0.05), f"{name}: nominal output is {actual_v:.3f} V, expected {expected_v:.3f} V")
    print(f"PASS: {name} nominal divider output = {actual_v:.3f} V")


def main():
    connectivity = load_json(CONNECTIVITY_PATH)
    response = load_json(COMPONENTS_PATH)
    require(response.get("ok") is True, "Component export response is not successful")

    components = [component for component in response["result"]["components"] if component.get("componentType") == "part"]
    component_map = {component["designator"]: component for component in components}
    require(len(component_map) == len(components), "Duplicate component designators found")

    net_map = {net["id"]: net["name"] for net in connectivity["nets"]}
    require(len(net_map) == len(connectivity["nets"]), "Duplicate net IDs found")
    require(len(set(net_map.values())) == len(net_map), "Duplicate net names found")
    anonymous_prefixes = ("$", "N$", "GGE", "Net-")
    anonymous = [name for name in net_map.values() if name.startswith(anonymous_prefixes)]
    require(not anonymous, f"Anonymous nets found: {anonymous}")
    print("PASS: Net names are unique and non-anonymous")

    exported_refs = {component["ref"] for component in connectivity["components"]}
    require(exported_refs == set(component_map), "Component sets differ between the two exports")

    floating = []
    intentional_nc = []
    component_pin_nets = {}
    for designator, component in component_map.items():
        for pin in component.get("pins", []):
            key = (designator, str(pin["pinNumber"]))
            net = pin.get("net") or ""
            if pin.get("noConnected"):
                intentional_nc.append(key)
            elif not net:
                floating.append(key)
            else:
                component_pin_nets[key] = net

    require(not floating, f"Unmarked floating pins found: {floating}")
    require(intentional_nc == [("U1", "5")], f"Unexpected NC pins: {intentional_nc}")
    print("PASS: No unmarked floating pins; U1 pin 5 (EN) is the sole intentional NC")

    connectivity_pin_nets = {}
    for connection in connectivity["connections"]:
        require(connection["netId"] in net_map, f"Unknown net ID: {connection['netId']}")
        designator = connection["componentId"].removeprefix("cmp-")
        key = (designator, str(connection["pinNumber"]))
        require(key not in connectivity_pin_nets, f"Pin occurs in multiple nets: {key}")
        connectivity_pin_nets[key] = net_map[connection["netId"]]
    require(connectivity_pin_nets == component_pin_nets, "Connectivity and component exports disagree at pin level")
    print("PASS: Both exports agree on every connected component pin")

    expected_values = {"R1": "100kΩ", "R2": "13.3kΩ", "R3": "45.3kΩ", "R4": "10kΩ", "F1": "TBD_MEASURE", "F2": "TBD_MEASURE", "F3": "TBD_MEASURE"}
    for designator, expected in expected_values.items():
        actual = component_value(component_map[designator])
        require(actual == expected, f"{designator}: value is {actual!r}, expected {expected!r}")

    for designator in ("F1", "F2", "F3"):
        component = component_map[designator]
        require(component["addIntoBom"] is False, f"{designator} must be excluded from BOM")
        require(component["addIntoPcb"] is False, f"{designator} must be excluded from PCB")
    print("PASS: Critical values and provisional fuse exclusions match")

    expected_parts = {"U1": ("TPS54302DDCT", "C129370"), "U2": ("TLV62569DBVT", "C2071150"), "L1": ("CKST0603-10uH/M", "C3002639"), "L2": ("ZEYH0420-2.2UH", "C46634742")}
    for designator, (manufacturer_id, supplier_id) in expected_parts.items():
        component = component_map[designator]
        require(component.get("manufacturerId") == manufacturer_id, f"{designator} MPN mismatch")
        require(component.get("supplierId") == supplier_id, f"{designator} LCSC mismatch")
    print("PASS: Regulator and inductor identities match the reviewed baseline")

    verify_voltage(100e3, 13.3e3, 0.596, 5.077, "TPS54302 BUCK_5V")
    verify_voltage(45.3e3, 10e3, 0.6, 3.318, "TLV62569 3V3")

    golden = {
        "12V_IN": ["J1:1", "F1:1", "C9:1"],
        "GND": ["J1:2", "C9:2", "D2:2", "U1:1", "C1:2", "C2:2", "C4:2", "C5:2", "R2:2", "U2:2", "C6:2", "C7:2", "R4:2"],
        "F1_OUT": ["F1:2", "D1:2"],
        "12V_PROTECTED": ["D1:1", "D2:1", "U1:3", "C1:1", "C2:1", "F2:1"],
        "U1_SW": ["U1:2", "L1:1", "C3:2"],
        "U1_BOOT": ["U1:6", "C3:1"],
        "U1_FB": ["U1:4", "R1:2", "R2:1", "C8:2"],
        "BUCK_5V": ["L1:2", "C4:1", "C5:1", "R1:1", "C8:1", "F3:1", "D3:2"],
        "PUMP_FUSE_OUT": ["F2:2"],
        "SCALE_5V": ["F3:2"],
        "USB_5V": ["D4:2"],
        "LOGIC_5V": ["D3:1", "D4:1", "U2:1", "U2:4", "C6:1"],
        "U2_SW": ["U2:3", "L2:2"],
        "3V3": ["L2:1", "C7:1", "R3:1"],
        "U2_FB": ["U2:5", "R3:2", "R4:1"],
    }
    actual = {name: [] for name in golden}
    for (designator, pin_number), net_name in connectivity_pin_nets.items():
        if net_name in actual:
            actual[net_name].append(f"{designator}:{pin_number}")
    for net_name, expected_nodes in golden.items():
        require(set(actual[net_name]) == set(expected_nodes), f"Golden net mismatch: {net_name}")
    require(set(net_map.values()) == set(golden), "Net set differs from the golden netlist")
    print("PASS: Golden netlist matched exactly")

    print("ALL ARTIFACT CONSISTENCY CHECKS PASSED")
    print("NOTE: EasyEDA ERC/DRC, live-save state, ratings, and visual readability are not covered")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, TypeError, ValueError) as error:
        raise SystemExit(f"FAILED: {error}") from error
