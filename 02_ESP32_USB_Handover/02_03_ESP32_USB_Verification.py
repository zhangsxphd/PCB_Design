#!/usr/bin/env python3
"""Read-only verification of the saved Page-02 EasyEDA snapshot."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    with (HERE / name).open(encoding='utf-8') as f:
        return json.load(f)


def require(label, expected, actual):
    if expected != actual:
        raise AssertionError(f'{label}: EXPECTED={expected!r} ACTUAL={actual!r}')


def main():
    raw = load('02_09_LIVE_LIST.json')
    require('live list response', True, raw.get('ok'))
    parts = {p['designator']: p for p in raw['result']['components'] if p.get('componentType') == 'part'}
    expect = {p['designator']: p for p in load('02_COMPONENT_EXPECTATIONS.json')}
    require('exact component set', set(expect), set(parts))
    for d, e in expect.items():
        p = parts[d]
        require(f'{d} MPN', e['mpn'], p['manufacturerId'])
        require(f'{d} LCSC', e['lcsc'], p['supplierId'])
        require(f'{d} package', e['package'], p['footprint']['name'])
        require(f'{d} status', e['status'], p['otherProperty'].get('STATUS'))
        require(f'{d} value', e['value'], p['otherProperty'].get('Value', p.get('name', '')))
    for d, mpn, lcsc in [('U3', 'ESP32-C3-MINI-1-N4', 'C2838502'),
                          ('J2', 'U262-161N-4BVC11', 'C319148'),
                          ('U4', 'USBLC6-2SC6', 'C7519')]:
        require(f'{d} frozen MPN', mpn, parts[d]['manufacturerId'])
        require(f'{d} frozen LCSC', lcsc, parts[d]['supplierId'])

    pin = {(d, q['pinNumber']): q for d, p in parts.items() for q in p['pins']}
    actual_nc = {d: sorted([q['pinNumber'] for q in p['pins'] if q.get('noConnected')])
                 for d, p in parts.items() if any(q.get('noConnected') for q in p['pins'])}
    required_u3_nc = sorted('4 7 9 10 15 17 24 25 28 29 32 33 34 35'.split())
    require('U3 exact NC', required_u3_nc, actual_nc.get('U3'))
    require('J2 exact SBU NC', ['A8', 'B8'], actual_nc.get('J2'))
    require('no other NC', {'U3', 'J2'}, set(actual_nc))
    require('NC file', actual_nc, load('02_INTENTIONAL_NC.json'))
    grounds = set('1 2 11 14 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53'.split())
    official_u3_names = {str(n): ('GND' if str(n) in grounds else 'NC' if str(n) in required_u3_nc else name)
                         for n, name in {3: '3V3', 5: 'IO2', 6: 'IO3', 8: 'EN', 12: 'IO0', 13: 'IO1',
                                         16: 'IO10', 18: 'IO4', 19: 'IO5', 20: 'IO6', 21: 'IO7',
                                         22: 'IO8', 23: 'IO9', 26: 'IO18', 27: 'IO19',
                                         30: 'RXD0', 31: 'TXD0', **{n: '' for n in range(1, 54)
                                         if n not in (3, 5, 6, 8, 12, 13, 16, 18, 19, 20, 21,
                                                      22, 23, 26, 27, 30, 31)}}.items()}
    require('U3 official pin-name map', official_u3_names,
            {q['pinNumber']: q['pinName'] for q in parts['U3']['pins']})
    for n in grounds:
        require(f'U3:{n} ground', 'GND', pin['U3', n]['net'])
    for (d, n), q in pin.items():
        if not q.get('noConnected') and not q.get('net'):
            raise AssertionError(f'{d}:{n} floating: EXPECTED=named net ACTUAL=empty')

    conn = load('02_10_LIVE_CONNECTIVITY.json')
    names = {n['id']: n['name'] for n in conn['nets']}
    actual = {n: set() for n in names.values()}
    for c in conn['connections']:
        actual[names[c['netId']]].add(f"{c['componentId'].removeprefix('cmp-')}:{c['pinNumber']}")
    golden = {n: set(pins) for n, pins in load('02_GOLDEN_NETLIST.json').items()}
    require('Golden Netlist named nets', set(golden), set(actual))
    for n in golden:
        require(f'Golden Netlist {n}', golden[n], actual[n])
    required_nets = set('3V3 GND CHIP_EN GPIO2_STRAP GPIO8_STRAP GPIO9_BOOT SDA SCL ADC_12V_SENSE 12V_PROTECTED SCALE_RX SCALE_TX RUN_LED PUMP_LED PUMP_EN EXP_UART_RX EXP_UART_TX USB_5V CC1 CC2 USB_DP_PORT USB_DM_PORT USB_DP_ESD USB_DM_ESD USB_DP_MCU USB_DM_MCU'.split())
    require('required named nets present', set(), required_nets - set(actual))
    require('anonymous nets absent', [], sorted(n for n in actual if re.fullmatch(r'\$.*', n)))
    require('USB_5V and 3V3 separate', False, actual['USB_5V'] == actual['3V3'])
    require('LOGIC_5V absent from Page-02 pins', False, 'LOGIC_5V' in actual)

    u3 = {'3': '3V3', '5': 'GPIO2_STRAP', '6': 'ADC_12V_SENSE', '8': 'CHIP_EN',
          '12': 'SDA', '13': 'SCL', '16': 'PUMP_EN', '18': 'SCALE_RX', '19': 'SCALE_TX',
          '20': 'RUN_LED', '21': 'PUMP_LED', '22': 'GPIO8_STRAP', '23': 'GPIO9_BOOT',
          '26': 'USB_DM_MCU', '27': 'USB_DP_MCU', '30': 'EXP_UART_RX', '31': 'EXP_UART_TX'}
    for n, net in u3.items():
        require(f'U3:{n} GPIO map', net, pin['U3', n]['net'])
    j2 = {'A4B9': 'USB_5V', 'B4A9': 'USB_5V', 'A1B12': 'GND', 'B1A12': 'GND',
          'A5': 'CC1', 'B5': 'CC2', 'A6': 'USB_DP_PORT', 'B6': 'USB_DP_PORT',
          'A7': 'USB_DM_PORT', 'B7': 'USB_DM_PORT',
          '13': 'GND', '14': 'GND', '15': 'GND', '16': 'GND'}
    official_j2_names = {'A1B12': 'GND', 'A4B9': 'VBUS', 'A5': 'CC1', 'A6': 'DP1',
                         'A7': 'DN1', 'A8': 'SBU1', 'B4A9': 'VBUS', 'B1A12': 'GND',
                         'B5': 'CC2', 'B6': 'DP2', 'B7': 'DN2', 'B8': 'SBU2',
                         **{str(n): 'SHELL' for n in range(13, 17)}}
    require('J2 manufacturer pin-name map', official_j2_names,
            {q['pinNumber']: q['pinName'] for q in parts['J2']['pins']})
    for n, net in j2.items():
        require(f'J2:{n} USB-C map', net, pin['J2', n]['net'])
    u4 = {'1': 'USB_DP_PORT', '6': 'USB_DP_ESD', '3': 'USB_DM_PORT',
          '4': 'USB_DM_ESD', '2': 'GND', '5': 'USB_5V'}
    for n, net in u4.items():
        require(f'U4:{n} ESD channel', net, pin['U4', n]['net'])

    between = {'R5': {'CC1', 'GND'}, 'R6': {'CC2', 'GND'},
               'R7': {'USB_DM_ESD', 'USB_DM_MCU'}, 'R8': {'USB_DP_ESD', 'USB_DP_MCU'},
               'R9': {'3V3', 'CHIP_EN'}, 'C12': {'CHIP_EN', 'GND'}, 'SW1': {'CHIP_EN', 'GND'},
               'R10': {'3V3', 'GPIO2_STRAP'}, 'R11': {'3V3', 'GPIO8_STRAP'},
               'R12': {'3V3', 'GPIO9_BOOT'}, 'SW2': {'GPIO9_BOOT', 'GND'},
               'R15': {'PUMP_EN', 'GND'}, 'R16': {'SDA', '3V3'}, 'R17': {'SCL', '3V3'},
               'R18': {'12V_PROTECTED', 'ADC_12V_SENSE'},
               'R19': {'ADC_12V_SENSE', 'GND'}, 'C17': {'ADC_12V_SENSE', 'GND'},
               'C15': {'USB_5V', 'GND'}, 'C16': {'USB_5V', 'GND'},
               'C10': {'3V3', 'GND'}, 'C11': {'3V3', 'GND'},
               'C13': {'USB_DM_MCU', 'GND'}, 'C14': {'USB_DP_MCU', 'GND'}}
    for d, nets in between.items():
        require(f'{d} topology', nets, {q['net'] for q in parts[d]['pins']})
    require('CC nets distinct', False, actual['CC1'] == actual['CC2'])
    require('no capacitor on BOOT', [], [d for d, p in parts.items() if d.startswith('C') and any(q['net'] == 'GPIO9_BOOT' for q in p['pins'])])
    for d, value in {'R5': '5.1kΩ', 'R6': '5.1kΩ', 'R7': '22Ω', 'R8': '22Ω',
                     'R9': '10kΩ', 'R10': '10kΩ', 'R11': '10kΩ', 'R12': '10kΩ', 'R15': '10kΩ'}.items():
        require(f'{d} resistance', value, parts[d]['otherProperty'].get('Value'))
    for d in ('C13', 'C14', 'R16', 'R17'):
        require(f'{d} DNP', 'DNP', parts[d]['otherProperty'].get('ASSEMBLY_DEFAULT'))
        require(f'{d} BOM exclusion', False, parts[d]['addIntoBom'])
    for d in ('R18', 'R19'):
        p = parts[d]
        require(f'{d} pending value', 'TBD_CALC', p['otherProperty'].get('Value'))
        require(f'{d} pending status', 'WAIT_INPUT_MAX', p['otherProperty'].get('STATUS'))
        require(f'{d} PCB hold', 'TRUE', p['otherProperty'].get('DO_NOT_RELEASE_TO_PCB'))
        require(f'{d} BOM excluded', False, p['addIntoBom'])
        require(f'{d} PCB excluded', False, p['addIntoPcb'])

    bridge = load('02_11_LIVE_BRIDGE_CHECK.json')['result']['summary']
    for key in ('bridges', 'orphans', 'orphanFlags', 'orphanTrees'):
        require(f'bridge {key}', 0, bridge[key])
    check = load('02_12_LIVE_SCH_CHECK.json')['result']['summary']
    for key in ('floatingPins', 'geomNetMismatches', 'netMarkerMismatches', 'multiNetWires',
                'wireOverPins', 'zeroLengthWires', 'danglingWires', 'titleblockOverlaps', 'markerOverlaps'):
        require(f'check {key}', 0, check[key])
    print(f'PASS Page-02 electrical snapshot: {len(parts)} parts, {len(actual)} nets, {len(conn["connections"])} pin connections')
    print('PASS Golden Netlist, identities, GPIO/USB/CC/EN/BOOT/ADC/NC, bridge and electrical checks')


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, KeyError, TypeError, ValueError) as e:
        raise SystemExit(f'FAIL: {e}')
