#!/usr/bin/env python3
"""Generate SVG previews of the custom parts from their parameters.
Keeps the previews in sync with the .scad models. Re-run after changing dims:
    python3 cad/gen_previews.py
Outputs: cad/adapter-plate.svg, cad/battery-enclosure.svg  (pure stdlib).
"""
import math

# --- params mirror the .scad defaults; update together (all mm) ---
ADAPTER = dict(plate_OD=200, plate_t=16, motor_bc=150, motor_bolts=6, motor_bolt_d=9,
               motor_reg_d=110, bell_bc=170, bell_bolts=8, bell_bolt_d=11, bore_d=60)
ENC = dict(name="MAIN box (8 mod)", modules_x=2, modules_y=2, layers=2,
           mod_L=685, mod_W=300, mod_H=85, clear=8, wall_t=3, flange_w=25, vents=2)


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'font-family="Helvetica,Arial,sans-serif">{body}</svg>\n')


def adapter_svg(p):
    W, H, cx, cy = 540, 440, 240, 235
    s = 320.0 / p['plate_OD']
    e = [f'<rect width="{W}" height="{H}" fill="#fbfbf9"/>',
         '<text x="20" y="30" font-size="18" font-weight="bold" fill="#222">Adapter plate — front view (preview)</text>',
         '<text x="20" y="49" font-size="11" fill="#888">Placeholder dims from adapter-plate.scad — update after measuring (step 000/007).</text>',
         f'<circle cx="{cx}" cy="{cy}" r="{p["plate_OD"]/2*s:.1f}" fill="#eef1f4" stroke="#5b6b78" stroke-width="2"/>']
    if p['motor_reg_d'] > 0:
        e.append(f'<circle cx="{cx}" cy="{cy}" r="{p["motor_reg_d"]/2*s:.1f}" fill="none" stroke="#aaa" stroke-dasharray="5 4"/>')
    e.append(f'<circle cx="{cx}" cy="{cy}" r="{p["bore_d"]/2*s:.1f}" fill="#fff" stroke="#5b6b78" stroke-width="1.5"/>')
    e.append(f'<circle cx="{cx}" cy="{cy}" r="{p["motor_bc"]/2*s:.1f}" fill="none" stroke="#1565c0" stroke-width="0.7" stroke-dasharray="3 3"/>')
    for i in range(p['motor_bolts']):
        a = 2*math.pi*i/p['motor_bolts'] - math.pi/2
        e.append(f'<circle cx="{cx+math.cos(a)*p["motor_bc"]/2*s:.1f}" cy="{cy+math.sin(a)*p["motor_bc"]/2*s:.1f}" r="{p["motor_bolt_d"]/2*s:.1f}" fill="#1565c0"/>')
    e.append(f'<circle cx="{cx}" cy="{cy}" r="{p["bell_bc"]/2*s:.1f}" fill="none" stroke="#2e7d32" stroke-width="0.7" stroke-dasharray="3 3"/>')
    for i in range(p['bell_bolts']):
        a = 2*math.pi*i/p['bell_bolts'] - math.pi/2 + math.pi/p['bell_bolts']
        e.append(f'<circle cx="{cx+math.cos(a)*p["bell_bc"]/2*s:.1f}" cy="{cy+math.sin(a)*p["bell_bc"]/2*s:.1f}" r="{p["bell_bolt_d"]/2*s:.1f}" fill="none" stroke="#2e7d32" stroke-width="2"/>')
    e += [f'<line x1="{cx-9}" y1="{cy}" x2="{cx+9}" y2="{cy}" stroke="#c0392b"/>',
          f'<line x1="{cx}" y1="{cy-9}" x2="{cx}" y2="{cy+9}" stroke="#c0392b"/>']
    rows = [("Outer ⌀", f"{p['plate_OD']} mm"), ("Thickness", f"{p['plate_t']} mm"),
            ("Motor BC", f"{p['motor_bc']} ({p['motor_bolts']}× ⌀{p['motor_bolt_d']})"),
            ("Bell BC", f"{p['bell_bc']} ({p['bell_bolts']}× ⌀{p['bell_bolt_d']})"),
            ("Bore ⌀", f"{p['bore_d']} mm"), ("Register ⌀", f"{p['motor_reg_d']} mm")]
    e.append('<text x="430" y="95" font-size="12" font-weight="bold" fill="#333">Dims</text>')
    for j, (k, v) in enumerate(rows):
        e.append(f'<text x="430" y="{118+j*20}" font-size="11" fill="#444">{k}: {v}</text>')
    e += [f'<circle cx="30" cy="{H-26}" r="6" fill="#1565c0"/><text x="44" y="{H-22}" font-size="11" fill="#333">motor bolts</text>',
          f'<circle cx="150" cy="{H-26}" r="6" fill="none" stroke="#2e7d32" stroke-width="2"/><text x="164" y="{H-22}" font-size="11" fill="#333">bellhousing bolts</text>']
    return svg(W, H, ''.join(e))


def enclosure_svg(p):
    in_L = p['modules_x']*p['mod_L'] + (p['modules_x']+1)*p['clear']
    in_W = p['modules_y']*p['mod_W'] + (p['modules_y']+1)*p['clear']
    ext_L, ext_W = in_L + 2*p['wall_t'], in_W + 2*p['wall_t']
    W, H = 680, 380
    s = 560.0 / ext_L
    ox, oy = 60, 110
    e = [f'<rect width="{W}" height="{H}" fill="#fbfbf9"/>',
         f'<text x="20" y="30" font-size="18" font-weight="bold" fill="#222">Battery enclosure — top view: {p["name"]}</text>',
         '<text x="20" y="49" font-size="11" fill="#888">From battery-enclosure.scad — confirm external dims fit the measured bay (battery-fit.md).</text>',
         f'<rect x="{ox-p["flange_w"]*s:.1f}" y="{oy:.1f}" width="{(ext_L+2*p["flange_w"])*s:.1f}" height="{ext_W*s:.1f}" fill="#dfe7ec" stroke="#5b6b78"/>',
         f'<rect x="{ox:.1f}" y="{oy:.1f}" width="{ext_L*s:.1f}" height="{ext_W*s:.1f}" fill="#eef1f4" stroke="#5b6b78" stroke-width="2"/>',
         f'<rect x="{ox+p["wall_t"]*s:.1f}" y="{oy+p["wall_t"]*s:.1f}" width="{in_L*s:.1f}" height="{in_W*s:.1f}" fill="#fff" stroke="#9aa6ad"/>']
    for xi in range(p['modules_x']):
        for yi in range(p['modules_y']):
            mx = ox + (p['wall_t']+p['clear']+xi*(p['mod_L']+p['clear']))*s
            my = oy + (p['wall_t']+p['clear']+yi*(p['mod_W']+p['clear']))*s
            e.append(f'<rect x="{mx:.1f}" y="{my:.1f}" width="{p["mod_L"]*s:.1f}" height="{p["mod_W"]*s:.1f}" fill="#1976d2" fill-opacity="0.5" stroke="#0d47a1"/>')
    for v in range(1, p['vents']+1):
        vx = ox + v*ext_L*s/(p['vents']+1)
        e.append(f'<circle cx="{vx:.1f}" cy="{oy:.1f}" r="5" fill="#fff" stroke="#5b6b78"/>')
        e.append(f'<circle cx="{vx:.1f}" cy="{oy+ext_W*s:.1f}" r="5" fill="#fff" stroke="#5b6b78"/>')
    e.append(f'<text x="{ox:.0f}" y="{oy+ext_W*s+24:.0f}" font-size="12" fill="#0d47a1">'
             f'external {ext_L:.0f} × {ext_W:.0f} mm · {p["modules_x"]}×{p["modules_y"]} grid × {p["layers"]} layer(s) '
             f'= {p["modules_x"]*p["modules_y"]*p["layers"]} modules · flanges to frame rails</text>')
    e.append(f'<text x="{ox:.0f}" y="{oy+ext_W*s+44:.0f}" font-size="11" fill="#888">'
             f'○ = vent port · blue = module footprint · grey lip = mounting flange</text>')
    return svg(W, H, ''.join(e))


if __name__ == "__main__":
    open("cad/adapter-plate.svg", "w").write(adapter_svg(ADAPTER))
    open("cad/battery-enclosure.svg", "w").write(enclosure_svg(ENC))
    print("wrote cad/adapter-plate.svg, cad/battery-enclosure.svg")
