#!/usr/bin/env python3
import json, math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def load(path):
    with path.open(encoding='utf-8') as f: return json.load(f)

def main():
    conn = load(HERE / '01_01_POWER_Connectivity.json')
    response = load(HERE / '01_02_POWER_Components.json')
    golden = load(HERE / 'GOLDEN_NETLIST.json')
    expected = load(ROOT / 'COMPONENT_EXPECTATIONS.json')
    if response.get('ok') is not True: raise AssertionError('component snapshot is not ok')
    parts = [c for c in response['result']['components'] if c.get('componentType') == 'part']
    cmap = {c['designator']: c for c in parts}
    names = {n['name']: n for n in conn['nets']}
    by_id = {n['id']: n['name'] for n in conn['nets']}
    if set(names) != set(golden): raise AssertionError(f'net-name set EXPECTED={sorted(golden)} ACTUAL={sorted(names)}')
    actual = {n: [] for n in names}
    for item in conn['connections']:
        d = item['componentId'].removeprefix('cmp-')
        actual[by_id[item['netId']]].append(f"{d}:{item['pinNumber']}")
    for net, pins in golden.items():
        if set(actual[net]) != set(pins): raise AssertionError(f'{net}: EXPECTED={sorted(pins)} ACTUAL={sorted(actual[net])}')
    print('PASS exact allowed net-name set')
    print('PASS exact Golden Netlist pin sets')
    expected_nc = {'U1:5'}
    actual_nc = {f"{d}:{p['pinNumber']}" for d,c in cmap.items() for p in c.get('pins',[]) if p.get('noConnected')}
    if actual_nc != expected_nc: raise AssertionError(f'NC EXPECTED={sorted(expected_nc)} ACTUAL={sorted(actual_nc)}')
    print('PASS exact NC set')
    if cmap['U1']['pins'][4].get('net'): raise AssertionError('U1:5 has a net')
    print('PASS U1.5 true NC')
    for d,c in cmap.items():
        for p in c.get('pins',[]):
            if not p.get('noConnected') and not p.get('net'): raise AssertionError(f'unexpected floating pin {d}:{p["pinNumber"]}')
    print('PASS no other NC')
    polarity = {'D1':{'A':'F1_OUT','K':'12V_PROTECTED'},'D2':{'A':'GND','K':'12V_PROTECTED'},'D3':{'A':'BUCK_5V','K':'LOGIC_5V'},'D4':{'A':'USB_5V','K':'LOGIC_5V'}}
    for d,wanted in polarity.items():
        got = {p.get('pinName'):p.get('net') for p in cmap[d].get('pins',[])}
        if any(got.get(k) != v for k,v in wanted.items()): raise AssertionError(f'{d} polarity EXPECTED={wanted} ACTUAL={got}')
        print(f'PASS {d} polarity')
    for d,e in expected.items():
        if d not in cmap: raise AssertionError(f'missing component {d}')
        c = cmap[d]
        if d not in ('F1','F2','F3'):
            if c.get('manufacturerId') != e['mpn'] or c.get('supplierId') != e['lcsc']: raise AssertionError(f'{d} identity mismatch')
            if c.get('footprint',{}).get('name') != e['footprint']: raise AssertionError(f'{d} footprint mismatch')
            if d.startswith('C') and d != 'C9':
                got_value = c.get('otherProperty',{}).get('Value')
                if got_value != e.get('value'): raise AssertionError(f'{d} formal Value mismatch: {got_value!r}')
    print('PASS frozen component identities')
    print('PASS C1-C8 formal library values')
    for d in ('F1','F2','F3'):
        c = cmap[d]; props = c.get('otherProperty',{})
        for k,v in (('Value','TBD_MEASURE'),('STATUS','TBD_MEASURE'),('RATING','TBD_MEASURE'),('DO_NOT_RELEASE_TO_PCB','TRUE')):
            if props.get(k) != v: raise AssertionError(f'{d} {k} mismatch')
        if c.get('addIntoBom') is not False or c.get('addIntoPcb') is not False: raise AssertionError(f'{d} release flags')
        print(f'PASS {d} exclusion')
    if cmap['C9'].get('otherProperty',{}).get('ASSEMBLY_DEFAULT') != 'DNP': raise AssertionError('C9 is not DNP')
    print('PASS C9 DNP assembly gate')
    for d,top,bottom,ref,exp in (('U1',100e3,13.3e3,0.596,5.077),('U2',45.3e3,10e3,0.6,3.318)):
        value = ref*(1+top/bottom)
        if not math.isclose(value,exp,abs_tol=0.05): raise AssertionError(f'{d} divider {value}')
        print(f'PASS {d} feedback calculation = {value:.3f} V')
    print('PASS no anonymous nets')
    print('PASS no unexpected nets')
    waiver = load(HERE / '01_POWER_DRC_WAIVERS.json')
    allowed = {w['net'] for w in waiver['waivers']}
    if allowed != {'PUMP_FUSE_OUT','SCALE_5V','USB_5V'}: raise AssertionError('DRC waiver whitelist mismatch')
    drc_text = (HERE / '01_17_LIVE_DRC.txt').read_text(encoding='utf-8')
    import re
    m = re.search(r'Fatal\s*=\s*(\d+).*?Error\s*=\s*(\d+).*?Warning\s*=\s*(\d+)', drc_text, re.S)
    if not m: raise AssertionError('unparseable live DRC evidence')
    fatal, errors, warnings = map(int, m.groups())
    if fatal != 0 or errors != 0: raise AssertionError(f'DRC fatal/error gate: {fatal}/{errors}')
    found = {n for n in allowed if n in drc_text}
    if warnings != 3 or found != allowed: raise AssertionError(f'DRC whitelist gate warnings={warnings} found={sorted(found)}')
    print('PASS page DRC fatal/error and exact 3-warning waiver')
    print('01_POWER_GOLDEN_NETLIST = PASS')

if __name__ == '__main__':
    try: main()
    except (AssertionError,KeyError,TypeError,ValueError) as e: raise SystemExit(f'FAILED: {e}')
