"""Urbiva GitHub and developer brand kit generator.

Every graphic is composed from the approved master geometry in URBIVA_Logo_Package v1.0
(icon and wordmark paths are copied verbatim, only translated and scaled uniformly),
the module icons from src/components/Icon.tsx, and the pilot network coordinates from
src/data/pilot-network.ts. Output: SVG masters in svg/, PNG renders in png/ (rsvg-convert).
"""
import os, re, subprocess, json

PKG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logos")
OUT = os.path.dirname(os.path.abspath(__file__))
SVG = os.path.join(OUT, "svg"); PNG = os.path.join(OUT, "png")
os.makedirs(SVG, exist_ok=True); os.makedirs(PNG, exist_ok=True)

# ---------- brand ----------
MID, LIME, POR, IRIS, LAV, SEC = "#241B42", "#D5FF66", "#F7F5F0", "#7966EC", "#B9B1CE", "#655A7D"
DARK = dict(bg=MID, surface="#2B2250", raised="#342A5E", line="#43386F", grid="#2E2552", text=POR, text2=LAV, text3="#A39AC4",
            accent=LIME, route=LIME, route2=LAV, warn="#FFC861", danger="#FF8A7A", icon=LIME, word=POR, info="#A79BF5")
LIGHT = dict(bg=POR, surface="#FFFFFF", raised="#FFFFFF", line="#CFC8BA", grid="#E9E4DA", text=MID, text2=SEC, text3="#6E6680",
             accent=MID, route=IRIS, route2=SEC, warn="#7A4F00", danger="#B42318", icon=MID, word=MID, info="#5B47D6")

def read(p): return open(p, encoding="utf-8").read()
lock = read(f"{PKG}/L07_Dark-Mode-Transparent/URBIVA_L07_Dark-Mode-Transparent.svg")
ICON_D = re.search(r'<path id="icon" fill="[^"]+" d="([^"]+)"', lock).group(1)
WORD_D = re.search(r'<path id="wordmark" fill="[^"]+" d="([^"]+)"', lock).group(1)
LOCK_W, LOCK_H = 321.174, 100.0          # L07 viewBox, icon + wordmark
ICON_W, ICON_H = 106.186, 100.0          # icon bbox in master units

def icon(x, y, h, fill):
    s = h / ICON_H
    return f'<path transform="translate({x:.2f},{y:.2f}) scale({s:.6f})" fill="{fill}" d="{ICON_D}"/>'

def lockup(x, y, h, icon_fill, word_fill):
    s = h / LOCK_H
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.6f})">'
            f'<path fill="{icon_fill}" d="{ICON_D}"/><path fill="{word_fill}" d="{WORD_D}"/></g>')

ICONS = {
 "route": '<circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h7a3.5 3.5 0 0 0 0-7H9a3.5 3.5 0 0 1 0-7h7"/>',
 "camera": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
 "layers": '<path d="M12 3 2.5 8 12 13l9.5-5z"/><path d="M2.5 13 12 18l9.5-5"/>',
 "play": '<path d="M7 5l12 7-12 7z"/>',
 "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 15.5l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7z"/>',
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "map": '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/>',
}
def uicon(name, x, y, size, color, sw=1.75):
    s = size / 24
    return (f'<g transform="translate({x},{y}) scale({s:.4f})" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')

# pilot network (src/data/pilot-network.ts)
N = {"N1":(80,440),"N2":(220,440),"N3":(360,440),"N4":(500,440),"N5":(220,320),"N6":(360,320),"N7":(500,320),"N8":(640,320),
     "N9":(220,200),"N10":(360,200),"N11":(500,200),"N12":(580,200),"N13":(640,200),"N14":(430,260),"N15":(360,540),"N16":(500,540),"N17":(640,440)}
E = [("N2","N3"),("N3","N4"),("N4","N7"),("N7","N11"),("N2","N5"),("N5","N6"),("N2","N14"),("N6","N10"),("N10","N11"),("N11","N12"),
     ("N13","N8"),("N8","N17"),("N6","N7"),("N5","N9"),("N9","N10"),("N7","N8"),("N1","N2"),("N3","N15"),("N4","N17"),("N15","N16"),("N14","N11"),("N12","N13")]
SUITABLE = ["N2","N5","N6","N10","N11"]; SHORTEST = ["N2","N14","N11"]

def network(t, ox, oy, sc, opacity=1.0, highlight=True):
    out = [f'<g opacity="{opacity}">']
    for a, b in E:
        (x1,y1),(x2,y2) = N[a], N[b]
        out.append(f'<line x1="{ox+x1*sc:.1f}" y1="{oy+y1*sc:.1f}" x2="{ox+x2*sc:.1f}" y2="{oy+y2*sc:.1f}" stroke="{t["line"]}" stroke-width="{max(2,6*sc):.1f}" stroke-linecap="round"/>')
    if highlight:
        pts = " ".join(f"{ox+N[n][0]*sc:.1f},{oy+N[n][1]*sc:.1f}" for n in SHORTEST)
        out.append(f'<polyline points="{pts}" fill="none" stroke="{t["route2"]}" stroke-width="{max(2,5*sc):.1f}" stroke-dasharray="{10*sc:.1f} {12*sc:.1f}" stroke-linecap="round"/>')
        pts = " ".join(f"{ox+N[n][0]*sc:.1f},{oy+N[n][1]*sc:.1f}" for n in SUITABLE)
        out.append(f'<polyline points="{pts}" fill="none" stroke="{t["route"]}" stroke-width="{max(3,9*sc):.1f}" stroke-linejoin="round" stroke-linecap="round"/>')
        for n in N:
            x, y = ox+N[n][0]*sc, oy+N[n][1]*sc
            r = max(3, 7*sc)
            on = n in SUITABLE
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{t["bg"]}" stroke="{t["route"] if on else t["line"]}" stroke-width="{max(1.5,3*sc):.1f}"/>')
        sx, sy = ox+N["N2"][0]*sc, oy+N["N2"][1]*sc
        out.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{max(6,13*sc):.1f}" fill="{t["route"]}"/>')
        hx, hy = ox+N["N11"][0]*sc, oy+N["N11"][1]*sc
        out.append(hexagon(hx, hy, max(9,20*sc), t["text"], t["bg"]))
    out.append('</g>')
    return "\n".join(out)

def hexagon(cx, cy, r, fill, stroke=None):
    import math
    pts = " ".join(f"{cx + r*math.cos(math.radians(90+60*i)):.1f},{cy + r*math.sin(math.radians(90+60*i)):.1f}" for i in range(6))
    st = f' stroke="{stroke}" stroke-width="3"' if stroke else ""
    return f'<polygon points="{pts}" fill="{fill}"{st}/>'

def grid(t, w, h, step=40, op=1):
    lines = [f'<g stroke="{t["grid"]}" stroke-width="1" opacity="{op}">']
    for x in range(0, w+1, step): lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}"/>')
    for y in range(0, h+1, step): lines.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>')
    lines.append('</g>'); return "\n".join(lines)

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def text(x, y, s, size, fill, family="Inter", weight=400, anchor="start", ls=0, op=1):
    fam = {"Manrope":"Manrope", "Inter":"Inter", "Mono":"IBM Plex Mono"}[family]
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" letter-spacing="{ls}" opacity="{op}">{esc(s)}</text>')

def pill(x, y, label, fg, bg, stroke, size=18, pad=14, h=36, family="Mono"):
    w = int(len(label) * size * (0.62 if family=="Mono" else 0.56)) + pad*2
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{bg}" stroke="{stroke}" stroke-width="1.5"/>'
            + text(x+pad, y+h/2+size*0.36, label, size, fg, family, 500)), w

def svg(name, w, h, body, title):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
         f'<title>{esc(title)}</title>\n{body}\n</svg>\n')
    open(os.path.join(SVG, name + ".svg"), "w", encoding="utf-8").write(s)
    return name

def render(name, w=None, h=None, out=None):
    args = ["rsvg-convert", os.path.join(SVG, name + ".svg"), "-o", os.path.join(PNG, (out or name) + ".png")]
    if w: args[1:1] = ["-w", str(w)]
    if h: args[1:1] = ["-h", str(h)]
    subprocess.run(args, check=True)

made = []
# ---------- A. avatar (1024) ----------
def avatar(name, bg, fill, title):
    S = 1024; ih = 560  # icon height; width = 560*1.0619 = 595, inside the 724 px circle-safe square
    iw = ih * ICON_W / ICON_H
    # optical centring: the mark is visually heavier at the bottom blocks, nudge up 8 px
    x = (S - iw) / 2; y = (S - ih) / 2 - 8
    body = (f'<rect width="{S}" height="{S}" fill="{bg}"/>' if bg else "") + icon(x, y, ih, fill)
    made.append(svg(name, S, S, body, title))
avatar("urbiva-avatar-dark", MID, LIME, "Urbiva avatar, Volt Lime icon on Midnight Violet")
avatar("urbiva-avatar-light", POR, MID, "Urbiva avatar, Midnight Violet icon on Porcelain White")
avatar("urbiva-avatar-transparent", None, LIME, "Urbiva avatar, Volt Lime icon, transparent")
avatar("urbiva-avatar-mono", "#FFFFFF", "#000000", "Urbiva avatar, monochrome black on white")
# circular crop preview + 64 px preview sheet
def crop_preview():
    W, H = 1400, 620; t = DARK
    b = [f'<rect width="{W}" height="{H}" fill="#0F0B1E"/>', grid(t, W, H, 40, 0.6)]
    b.append(text(60, 70, "GitHub circular crop preview", 28, POR, "Manrope", 700))
    b.append(text(60, 104, "Safe area: the icon stays inside the inscribed circle with 18 % margin.", 18, LAV))
    cx, cy, r = 320, 360, 200
    b.append(f'<clipPath id="c"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>')
    ih = 560 * (2*r/1024); iw = ih * ICON_W / ICON_H
    b.append(f'<g clip-path="url(#c)"><rect x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" fill="{MID}"/>{icon(cx-iw/2, cy-ih/2-8*(2*r/1024), ih, LIME)}</g>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LAV}" stroke-width="2" stroke-dasharray="6 8"/>')
    x0 = 640
    b.append(text(x0, 190, "Small size check", 22, POR, "Manrope", 700))
    for i, sz in enumerate([64, 40, 32, 20]):
        x = x0 + sum([64, 40, 32, 20][:i]) + i*40; y = 230
        sc = sz / 1024; ih2 = 560*sc; iw2 = ih2*ICON_W/ICON_H
        b.append(f'<clipPath id="s{i}"><circle cx="{x+sz/2}" cy="{y+sz/2}" r="{sz/2}"/></clipPath>')
        b.append(f'<g clip-path="url(#s{i})"><rect x="{x}" y="{y}" width="{sz}" height="{sz}" fill="{MID}"/>{icon(x+(sz-iw2)/2, y+(sz-ih2)/2, ih2, LIME)}</g>')
        b.append(text(x, y+sz+28, f"{sz} px", 14, LAV, "Mono"))
    b.append(text(x0, 400, "Light reversed", 22, POR, "Manrope", 700))
    for i, sz in enumerate([64, 32]):
        x = x0 + i*110; y = 430; sc = sz/1024; ih2 = 560*sc; iw2 = ih2*ICON_W/ICON_H
        b.append(f'<clipPath id="l{i}"><circle cx="{x+sz/2}" cy="{y+sz/2}" r="{sz/2}"/></clipPath>')
        b.append(f'<g clip-path="url(#l{i})"><rect x="{x}" y="{y}" width="{sz}" height="{sz}" fill="{POR}"/>{icon(x+(sz-iw2)/2, y+(sz-ih2)/2, ih2, MID)}</g>')
        b.append(text(x, y+sz+28, f"{sz} px", 14, LAV, "Mono"))
    made.append(svg("urbiva-avatar-preview", W, H, "\n".join(b), "Urbiva avatar crop and small size preview"))
crop_preview()

# ---------- B. banner 1600x500 ----------
def banner(name, t, W=1600, H=500):
    b = [f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>', grid(t, W, H, 40, 0.9)]
    b.append(network(t, 880, -40, 1.12, 1.0))
    b.append(f'<rect x="0" y="0" width="760" height="{H}" fill="{t["bg"]}" opacity="0.82"/>')
    b.append(lockup(96, 88, 64, t["icon"], t["word"]))
    b.append(text(96, 252, "Intelligence for cities", 54, t["text"], "Manrope", 700, ls=-1))
    b.append(text(96, 316, "that work for everyone.", 54, t["text"], "Manrope", 700, ls=-1))
    b.append(text(96, 372, "AI-powered urban accessibility and infrastructure intelligence.", 22, t["text2"]))
    b.append(text(96, 428, "Every city. Every possibility.", 18, t["accent"], "Mono", 500, ls=1))
    made.append(svg(name, W, H, "\n".join(b), "Urbiva: Intelligence for cities that work for everyone. Every city. Every possibility."))
banner("urbiva-banner-dark", DARK); banner("urbiva-banner-light", LIGHT)

# ---------- C. social previews 1280x640 ----------
REPOS = {
 "urbiva-app": ("Human-centered urban intelligence platform for", "accessible navigation, AI-assisted reporting and", "infrastructure simulation.", ["Next.js", "TypeScript", "Tailwind", "Graph routing"], "network"),
 "urbiva-ai": ("Research and development of lightweight urban", "accessibility computer vision models.", "UVA-Net S10 · planned research", ["PyTorch (planned)", "≤ 10M params", "Local inference"], "vision"),
 "urbiva-brand": ("Official Urbiva brand assets, visual identity,", "design tokens and design guidelines.", "", ["Logo v1.0", "Tokens", "Figma DS v1.0"], "brand"),
 "urbiva-docs": ("Product specifications, architecture decisions,", "API documentation and engineering guides.", "", ["Architecture", "ADRs", "Roadmap"], "docs"),
 ".github": ("Building accessible, human-centered cities", "with artificial intelligence.", "", ["Organization profile", "Community health"], "network"),
}
def motif(kind, t, x, y, w, h):
    if kind == "network": return network(t, x, y, min(w/620, h/420), 1.0)
    if kind == "vision":
        out = [f'<g>']
        cols, rows, cs = 6, 4, min(w/6, h/4)
        for i in range(cols):
            for j in range(rows):
                out.append(f'<rect x="{x+i*cs+6:.0f}" y="{y+j*cs+6:.0f}" width="{cs-12:.0f}" height="{cs-12:.0f}" rx="10" fill="{t["surface"]}" stroke="{t["line"]}"/>')
        bx, by = x+cs*1.2, y+cs*1.1
        out.append(f'<rect x="{bx:.0f}" y="{by:.0f}" width="{cs*2.4:.0f}" height="{cs*1.6:.0f}" fill="none" stroke="{t["info"]}" stroke-width="3" stroke-dasharray="10 8"/>')
        out.append(f'<rect x="{bx:.0f}" y="{by-34:.0f}" width="210" height="30" rx="6" fill="{t["bg"]}" stroke="{t["info"]}" stroke-width="2"/>')
        out.append(text(bx+12, by-13, "stairs · estimate", 16, t["info"], "Mono", 500))
        for k in range(5):
            out.append(f'<line x1="{bx+12:.0f}" y1="{by+20+k*24:.0f}" x2="{bx+cs*2.4-12:.0f}" y2="{by+20+k*24:.0f}" stroke="{t["text3"]}" stroke-width="6" stroke-linecap="round" opacity="0.5"/>')
        out.append('</g>'); return "\n".join(out)
    if kind == "brand":
        out = []; ih = min(h*0.62, 240); iw = ih*ICON_W/ICON_H
        out.append(icon(x+w-iw, y+10, ih, t["accent"]))
        sw = [MID, LIME, POR, IRIS, LAV, SEC]
        for i, c in enumerate(sw):
            out.append(f'<rect x="{x+i*58}" y="{y+h-70}" width="50" height="50" rx="10" fill="{c}" stroke="{t["line"]}"/>')
        return "\n".join(out)
    if kind == "docs":
        out = []
        boxes = [(0,0,"Vision"),(1,0,"Graph"),(2,0,"Go"),(1,1,"Urban"),(2,1,"Impact")]
        bw, bh = w/3-24, 70
        for c, r, lab in boxes:
            bx, by = x+c*(bw+24), y+30+r*(bh+60)
            out.append(f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw:.0f}" height="{bh}" rx="12" fill="{t["surface"]}" stroke="{t["line"]}" stroke-width="1.5"/>')
            out.append(text(bx+18, by+43, lab, 22, t["text"], "Manrope", 700))
        for (c1,r1),(c2,r2) in [((0,0),(1,0)),((1,0),(2,0)),((1,0),(1,1)),((1,1),(2,1))]:
            x1 = x+c1*(bw+24)+(bw if c2>c1 else bw/2); y1 = y+30+r1*(bh+60)+(bh/2 if c2>c1 else bh)
            x2 = x+c2*(bw+24)+(0 if c2>c1 else bw/2); y2 = y+30+r2*(bh+60)+(bh/2 if c2>c1 else 0)
            out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{t["route"]}" stroke-width="3"/>')
        for k in range(4):
            out.append(f'<line x1="{x:.0f}" y1="{y+h-80+k*20:.0f}" x2="{x+w*(0.9-k*0.15):.0f}" y2="{y+h-80+k*20:.0f}" stroke="{t["text3"]}" stroke-width="6" stroke-linecap="round" opacity="0.45"/>')
        return "\n".join(out)
def social(repo, t, suffix):
    W, H = 1280, 640; d1, d2, d3, chips, kind = REPOS[repo]
    b = [f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>', grid(t, W, H, 40, 0.8)]
    b.append(f'<g>{motif(kind, t, 760, 120, 460, 400)}</g>')
    b.append(f'<rect x="0" y="0" width="720" height="{H}" fill="{t["bg"]}" opacity="0.86"/>')
    b.append(icon(72, 72, 64, t["icon"]))
    b.append(text(160, 104, "urbiva /", 26, t["text2"], "Mono", 500))
    b.append(text(72, 248, repo, 76, t["text"], "Manrope", 800, ls=-1.5))
    y = 316
    for line in (d1, d2, d3):
        if line: b.append(text(72, y, line, 26, t["text2"])); y += 38
    x = 72
    for c in chips:
        p, w = pill(x, 520, c, t["text"], t["surface"], t["line"], size=17); b.append(p); x += w + 12
    b.append(text(72, 600, "Every city. Every possibility.", 16, t["accent"], "Mono", 500, ls=1))
    made.append(svg(f"social-{repo.strip('.')}-{suffix}", W, H, "\n".join(b), f"{repo}: social preview"))
for r in REPOS: social(r, DARK, "dark")
for r in REPOS: social(r, LIGHT, "light")

# ---------- E. repository headers 1600x400 ----------
HEAD = {"urbiva-app": ("Application", "Go · Vision · Urban · Impact", "network"), "urbiva-ai": ("AI Research", "UVA-Net S10 · planned, not trained", "vision"),
        "urbiva-brand": ("Brand System", "Logo · colour · type · tokens", "brand"), "urbiva-docs": ("Documentation", "Product · architecture · decisions", "docs")}
def header(repo, t, suffix):
    W, H = 1600, 400; title, sub, kind = HEAD[repo]
    b = [f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>', grid(t, W, H, 40, 0.85)]
    b.append(f'<g>{motif(kind, t, 1000, 40, 520, 320)}</g>')
    b.append(f'<rect x="0" y="0" width="940" height="{H}" fill="{t["bg"]}" opacity="0.86"/>')
    b.append(lockup(88, 72, 48, t["icon"], t["word"]))
    b.append(text(88, 228, title, 64, t["text"], "Manrope", 800, ls=-1.2))
    b.append(text(88, 284, sub, 24, t["text2"]))
    b.append(text(88, 340, repo, 18, t["accent"], "Mono", 500, ls=1))
    made.append(svg(f"header-{repo}-{suffix}", W, H, "\n".join(b), f"{repo}: {title}"))
for r in HEAD: header(r, DARK, "dark"); header(r, LIGHT, "light")

# ---------- D. architecture 1600x900 ----------
def arch(t, suffix):
    W, H = 1600, 940
    b = [f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>', grid(t, W, H, 40, 0.6)]
    b.append(text(80, 96, "How Urbiva works", 44, t["text"], "Manrope", 800, ls=-1))
    b.append(text(80, 138, "From an observation on the street to a simulated infrastructure decision. Data in the current demo comes from a sample pilot network.", 20, t["text2"]))
    def box(x, y, w, h, title, lines, kind="impl", ic=None):
        stroke = t["route"] if kind == "impl" else t["text3"]
        dash = '' if kind == "impl" else ' stroke-dasharray="10 8"'
        s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{t["surface"]}" stroke="{stroke}" stroke-width="2"{dash}/>']
        tx = x+24
        if ic: s.append(uicon(ic, x+24, y+26, 28, t["route"] if kind=="impl" else t["text3"])); tx = x+66
        s.append(text(tx, y+50, title, 24, t["text"], "Manrope", 700))
        for i, l in enumerate(lines): s.append(text(x+24, y+90+i*28, l, 17, t["text2"]))
        return "\n".join(s)
    def arrow(x1, y1, x2, y2, kind="impl"):
        c = t["route"] if kind == "impl" else t["text3"]; dash = '' if kind == "impl" else ' stroke-dasharray="8 8"'
        import math; a = math.atan2(y2-y1, x2-x1); hx, hy = x2-14*math.cos(a), y2-14*math.sin(a)
        p1 = (hx-8*math.sin(a), hy+8*math.cos(a)); p2 = (hx+8*math.sin(a), hy-8*math.cos(a))
        return (f'<line x1="{x1}" y1="{y1}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{c}" stroke-width="3"{dash}/>'
                f'<polygon points="{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{c}"/>')
    y1 = 210
    b.append(box(80, y1, 310, 190, "Urban Observation", ["Resident photographs a", "barrier on a segment.", "Photo is re-encoded,", "EXIF and GPS removed."], ic="camera"))
    b.append(box(440, y1, 320, 190, "Urbiva Vision", ["Vision model estimate", "(today: Claude vision API)", "plus human confirmation.", "Manual fallback without AI."], ic="sparkle"))
    b.append(box(810, y1, 340, 190, "Verified Barrier Data", ["Reports: unverified,", "AI estimate, confirmed.", "Planner reviews in", "Urbiva Urban."], ic="check"))
    b.append(box(1200, y1, 320, 190, "Accessibility Graph", ["Nodes, segments, barriers.", "Passability per profile:", "ok, uncertain, unknown,", "blocked."], ic="map"))
    y2 = 500
    b.append(box(1200, y2, 320, 170, "Urbiva Go", ["Dijkstra: suitable route", "vs shortest route.", "Penalties for uncertainty."], ic="route"))
    b.append(box(840, y2, 300, 170, "Urbiva Urban", ["Metrics from the graph.", "Review and prioritise", "confirmed barriers."], ic="layers"))
    b.append(box(440, y2, 340, 170, "Urbiva Impact", ["simulateIntervention on a", "graph copy: 15 min reach,", "before and after."], ic="play"))
    b.append(box(80, y2, 300, 170, "UVA-Net S10", ["Planned local vision model", "≤ 10M parameters.", "Not trained yet."], kind="plan", ic="sparkle"))
    b.append(arrow(390, y1+95, 440, y1+95)); b.append(arrow(760, y1+95, 810, y1+95)); b.append(arrow(1150, y1+95, 1200, y1+95))
    b.append(arrow(1360, y1+190, 1360, y2)); b.append(arrow(1290, y1+190, 1060, y2))
    b.append(arrow(840, y2+85, 780, y2+85))
    b.append(arrow(230, y2, 560, y1+190, "plan"))
    ly = 760
    b.append(f'<rect x="80" y="{ly}" width="40" height="0" stroke="{t["route"]}" stroke-width="3"/>' + f'<line x1="80" y1="{ly}" x2="120" y2="{ly}" stroke="{t["route"]}" stroke-width="3"/>')
    b.append(text(136, ly+6, "Implemented in urbiva-app (MVP, sample pilot network)", 18, t["text2"]))
    b.append(f'<line x1="80" y1="{ly+40}" x2="120" y2="{ly+40}" stroke="{t["text3"]}" stroke-width="3" stroke-dasharray="8 8"/>')
    b.append(text(136, ly+46, "Planned research in urbiva-ai (no model, weights or results exist yet)", 18, t["text2"]))
    b.append(text(80, 880, "Every city. Every possibility.", 16, t["accent"], "Mono", 500, ls=1))
    made.append(svg(f"urbiva-architecture-{suffix}", W, H, "\n".join(b), "Urbiva architecture: observation, Vision, verified barriers, accessibility graph, Go, Urban, Impact; UVA-Net S10 planned"))
arch(DARK, "dark"); arch(LIGHT, "light")

# ---------- F. developer assets ----------
MODULES = [("Urbiva Go", "Accessible route navigation", ["Suitable vs shortest route", "Mobility profiles", "Segment-level trust"], "route"),
           ("Urbiva Vision", "AI-assisted barrier reporting", ["Photo to barrier estimate", "Human confirmation", "Manual fallback"], "camera"),
           ("Urbiva Urban", "Infrastructure intelligence dashboard", ["Graph-derived metrics", "Barrier review", "Verification states"], "layers"),
           ("Urbiva Impact", "Infrastructure intervention simulation", ["What-if on a graph copy", "15-minute reachability", "Before and after"], "play")]
def module_card(i, t, suffix):
    W, H = 760, 380; name, desc, bullets, ic = MODULES[i]
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="28" fill="{t["surface"]}" stroke="{t["line"]}" stroke-width="2"/>']
    b.append(f'<rect x="40" y="40" width="72" height="72" rx="36" fill="{t["raised"] if suffix=="dark" else t["bg"]}"/>' + uicon(ic, 58, 58, 36, t["route"]))
    b.append(text(40, 176, name, 40, t["text"], "Manrope", 800, ls=-0.8))
    b.append(text(40, 218, desc, 22, t["text2"]))
    for k, l in enumerate(bullets):
        b.append(uicon("check", 40, 252+k*36, 22, t["route"])); b.append(text(74, 270+k*36, l, 19, t["text"]))
    p, w = pill(W-40-150, 44, "IMPLEMENTED", t["route"], t["bg"], t["route"], size=14, h=30); b.append(p)
    made.append(svg(f"module-{name.split()[1].lower()}-{suffix}", W, H, "\n".join(b), f"{name}: {desc}"))
for i in range(4): module_card(i, DARK, "dark"); module_card(i, LIGHT, "light")
def divider(t, suffix):
    W, H = 1600, 48
    b = [f'<line x1="0" y1="24" x2="{W}" y2="24" stroke="{t["line"]}" stroke-width="2"/>']
    for k, x in enumerate(range(720, 881, 40)):
        b.append(f'<circle cx="{x}" cy="24" r="{7 if k==2 else 5}" fill="{t["bg"]}" stroke="{t["route"] if k==2 else t["line"]}" stroke-width="3"/>')
    b.append(f'<line x1="720" y1="24" x2="880" y2="24" stroke="{t["route"]}" stroke-width="4"/>')
    made.append(svg(f"divider-{suffix}", W, H, "\n".join(b), "Section divider"))
divider(DARK, "dark"); divider(LIGHT, "light")
STATUS = [("implemented", "IMPLEMENTED", "route"), ("sample", "SAMPLE DATA", "text2"), ("planned", "PLANNED", "text3"), ("research", "RESEARCH", "info")]
for key, lab, col in STATUS:
    for t, suffix in ((DARK, "dark"), (LIGHT, "light")):
        p, w = pill(2, 2, lab, t[col], t["bg"], t[col], size=15, h=32, pad=14)
        made.append(svg(f"status-{key}-{suffix}", w+4, 36, p, f"Status: {lab.title()}"))
def feature_template(t, suffix):
    W, H = 1600, 900
    b = [f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>', grid(t, W, H, 40, 0.7)]
    b.append(text(80, 110, "Feature title", 48, t["text"], "Manrope", 800, ls=-1))
    b.append(text(80, 156, "One sentence on what the feature does and for whom.", 22, t["text2"]))
    b.append(f'<rect x="80" y="210" width="1440" height="610" rx="24" fill="{t["surface"]}" stroke="{t["line"]}" stroke-width="2" stroke-dasharray="10 10"/>')
    b.append(text(800, 525, "Screenshot area 1440 × 610", 22, t["text3"], "Mono", 500, anchor="middle"))
    b.append(lockup(1360, 76, 36, t["icon"], t["word"]))
    made.append(svg(f"feature-template-{suffix}", W, H, "\n".join(b), "Feature preview template"))
feature_template(DARK, "dark"); feature_template(LIGHT, "light")

# ---------- render ----------
for n in made: render(n)
for v in ("dark", "light", "transparent", "mono"):
    render(f"urbiva-avatar-{v}", 512, 512, f"urbiva-avatar-{v}-512")
render("urbiva-avatar-dark", 64, 64, "urbiva-avatar-dark-64")
render("urbiva-banner-dark", 1280, 400, "urbiva-banner-dark-1280")
render("urbiva-banner-light", 1280, 400, "urbiva-banner-light-1280")
json.dump(sorted(made), open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
print(len(made), "SVG masters rendered")
