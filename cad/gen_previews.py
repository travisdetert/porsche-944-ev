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
# Dash layout (mm, origin top-left to match dash-panel.scad). Each gauge: (label, source, x, y, dia)
DASH = dict(w=380, h=170,
            big=[("MPH", "speedo · transaxle", 95, 92, 86), ("RPM x1000", "motor rpm", 285, 92, 86)],
            small=[("CHARGE %", "← fuel", 190, 50, 40), ("HV x100 V", "← oil press", 190, 104, 40),
                   ("BATT C", "← oil temp", 150, 148, 34), ("COOLANT", "native", 230, 148, 34)],
            lights=[("FAULT", "#c0392b"), ("BMS", "#e67e22"), ("12V", "#1565c0"), ("BRAKE", "#c0392b")])


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


def dashboard_svg(d):
    px, py, W, H = 20, 54, d['w'] + 40, d['h'] + 110
    e = [f'<rect width="{W}" height="{H}" fill="#1b1b1b"/>',
         '<text x="20" y="30" font-size="18" font-weight="bold" fill="#eee">Custom dash layout (preview) — repurposed EV gauges</text>',
         '<text x="20" y="48" font-size="11" fill="#999">Faces/panel per ADR-0012 · cut panel: dash-panel.scad · gauge map: dashboard-reuse.md</text>',
         f'<rect x="{px}" y="{py}" rx="10" width="{d["w"]}" height="{d["h"]}" fill="#222" stroke="#555" stroke-width="2"/>']
    for i, (lab, col) in enumerate(d['lights']):
        lx = px + 70 + i*74
        e.append(f'<circle cx="{lx}" cy="{py+15}" r="6" fill="{col}"/><text x="{lx+10}" y="{py+19}" font-size="9" fill="#bbb">{lab}</text>')

    def gauge(lab, src, x, y, dia, big):
        cx, cy, r = px + x, py + y, dia/2
        g = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#111" stroke="#999" stroke-width="2"/>']
        for t in range(11):
            a = math.radians(225 - t*270/10)
            g.append(f'<line x1="{cx+math.cos(a)*(r-3):.0f}" y1="{cy-math.sin(a)*(r-3):.0f}" '
                     f'x2="{cx+math.cos(a)*(r-8):.0f}" y2="{cy-math.sin(a)*(r-8):.0f}" stroke="#888"/>')
        if big:
            a = math.radians(225 - 6.5*270/10)
            g.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+math.cos(a)*(r-12):.0f}" y2="{cy-math.sin(a)*(r-12):.0f}" stroke="#e53935" stroke-width="2.5"/>')
            g.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="#e53935"/>')
        g.append(f'<text x="{cx}" y="{cy+r*0.5:.0f}" font-size="{12 if big else 9}" fill="#eee" text-anchor="middle" font-weight="bold">{lab}</text>')
        g.append(f'<text x="{cx}" y="{cy+r+12:.0f}" font-size="8" fill="#888" text-anchor="middle">{src}</text>')
        return ''.join(g)

    for lab, src, x, y, dia in d['big']:
        e.append(gauge(lab, src, x, y, dia, True))
    for lab, src, x, y, dia in d['small']:
        e.append(gauge(lab, src, x, y, dia, False))
    e.append(f'<text x="20" y="{H-14}" font-size="10" fill="#999">"←" = was-gas gauge, repurposed · print 1:1 as a face template · DXF panel from dash-panel.scad</text>')
    return svg(W, H, ''.join(e))


if __name__ == "__main__":
    open("cad/adapter-plate.svg", "w").write(adapter_svg(ADAPTER))
    open("cad/battery-enclosure.svg", "w").write(enclosure_svg(ENC))
    open("cad/dash-panel.svg", "w").write(dashboard_svg(DASH))
    print("wrote cad/adapter-plate.svg, cad/battery-enclosure.svg, cad/dash-panel.svg")
