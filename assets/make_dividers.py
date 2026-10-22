"""Three section dividers in a flat abstract wireframe style, each in a light and a dark version.
  divider-mesh-*.svg      a warped wireframe grid that ripples, with an orange disc and a dotted column
  divider-contours-*.svg  a twisting ribbon of contour lines, rings, triangles and crosses
  divider-moons-*.svg     half-moons with arc lines, dot rows that light up, stripes and hatching
Run: python3 assets/make_dividers.py
"""
import math, pathlib

HERE = pathlib.Path(__file__).parent
W, H = 1200, 150
MINT, VIOLET, TANGERINE, SUN, CORAL, TEAL = "#3DC593", "#7C6CFF", "#FF8A3D", "#FFD166", "#FF6B6B", "#1F9E95"
THEMES = {
    "light": dict(ink="#1B1726", line="#1B1726", paper="#FFFFFF", soft=".55"),
    "dark": dict(ink="#F3EEF8", line="#D9D2E6", paper="#0D1117", soft=".45"),
}
TAU = math.tau


def svg(body, label=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{label}">{body}</svg>')


def poly(pts):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def morph(frames, dur, extra=""):
    """A path whose d loops through the given frames (first frame repeated at the end)."""
    vals = ";".join(frames + [frames[0]])
    return f'<path d="{frames[0]}" {extra}><animate attributeName="d" values="{vals}" dur="{dur}s" repeatCount="indefinite"/></path>'


def float_y(dy, dur, begin=0):
    return f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {dy};0 0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite" additive="sum"/>'


def spin(cx, cy, dur, rev=False):
    a, b = (360, 0) if rev else (0, 360)
    return f'<animateTransform attributeName="transform" type="rotate" from="{a} {cx} {cy}" to="{b} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>'


def dots_row(x, y, n, gap, r, col, step=None, dur=3.0, vertical=False):
    """A row of dots; with step set, the dots light up one after another."""
    out = []
    for i in range(n):
        cx, cy = (x, y + i * gap) if vertical else (x + i * gap, y)
        anim = ""
        if step:
            anim = f'<animate attributeName="opacity" values=".25;1;.25" dur="{dur}s" begin="{i * step:.2f}s" repeatCount="indefinite"/>'
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity="{".25" if step else "1"}">{anim}</circle>')
    return "".join(out)


def cross(x, y, s, col, sw=3):
    return (f'<path d="M{x - s} {y - s} L{x + s} {y + s} M{x + s} {y - s} L{x - s} {y + s}" '
            f'stroke="{col}" stroke-width="{sw}" stroke-linecap="square"/>')


def hatch(x, y, w, h, col, gap=6, sw=1.4):
    lines = "".join(f'<line x1="{x + i}" y1="{y + h}" x2="{x + i + h * .6:.1f}" y2="{y}"/>' for i in range(0, int(w), gap))
    return f'<g stroke="{col}" stroke-width="{sw}">{lines}</g>'


def barcode(x, y, col, widths):
    out, cy = [], y
    for hgt, gap in widths:
        i = len(out)
        w2 = 30 + (i * 37) % 40                      # each stripe stretches to its own width, like an equaliser
        out.append(f'<rect x="{x}" y="{cy}" width="70" height="{hgt}" fill="{col}">'
                   f'<animate attributeName="width" values="70;{w2};70" dur="{3 + (i % 3) * .7:.1f}s" begin="{i * .2:.1f}s" repeatCount="indefinite"/></rect>')
        cy += hgt + gap
    return "".join(out)


def sparkle(x, y, s, col, d):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 -10 L2.5 -2.5 L10 0 L2.5 2.5 L0 10 L-2.5 2.5 L-10 0 L-2.5 -2.5 Z" fill="{col}">'
            f'<animate attributeName="opacity" values="0;1;0" dur="3s" begin="{d}s" repeatCount="indefinite"/></path></g>')


# ------------------------------------------------------------------ 1. wireframe mesh
def mesh_height(x, j, t):
    env = math.sin(math.pi * min(max((x - 300) / 620, 0), 1)) ** 1.3
    return env * (24 * math.sin(x * .011 + t + j * .22) + 12 * math.sin(x * .026 - t * 1.3 + j * .45))


def mesh(t):
    rows, xs = 13, range(300, 921, 12)
    frames_h = [[] for _ in range(rows)]
    phases = [0, TAU / 3, 2 * TAU / 3]
    vcols = list(range(300, 921, 20))
    frames_v = [[] for _ in vcols]
    for ph in phases:
        for j in range(rows):
            y0 = 40 + j * 4 + j * j * .28
            frames_h[j].append(poly([(x, y0 + mesh_height(x, j, ph)) for x in xs]))
        for k, x in enumerate(vcols):
            frames_v[k].append(poly([(x + (x - 610) * j * .012, 40 + j * 4 + j * j * .28 + mesh_height(x, j, ph)) for j in range(rows)]))
    stroke = f'fill="none" stroke="url(#mg{id(t) % 1000})" stroke-width=".9"'
    grid = "".join(morph(f, 9, stroke) for f in frames_h) + "".join(morph(f, 9, stroke) for f in frames_v)
    g = f'<defs><linearGradient id="mg{id(t) % 1000}" x1="0" x2="1"><stop offset="0" stop-color="{TEAL}"/><stop offset=".5" stop-color="{t["line"]}" stop-opacity="{t["soft"]}"/><stop offset="1" stop-color="{TANGERINE}"/></linearGradient></defs>'
    return svg(g + f'''
  <g>{barcode(40, 34, t["ink"], [(5, 4), (5, 4), (12, 4), (18, 5), (5, 4), (14, 4), (5, 4), (6, 0)])}</g>
  <g>{dots_row(150, 30, 6, 9, 2.4, TEAL)}{dots_row(210, 30, 6, 9, 2.4, TEAL)}</g>
  <circle cx="232" cy="96" r="38" fill="{TANGERINE}"/>
  <g fill="none" stroke="#FFFFFF" stroke-width="1.2" opacity=".9">
    {"".join(f'<path d="M{206 + i * 4} {70 + i * 2} C {214 + i * 4} {96 + i * 2}, {238 + i * 3} {110 + i}, {266 - i} {108 - i * 3}"/>' for i in range(6))}
  </g>
  <g>{float_y(-6, 5)}<circle cx="276" cy="58" r="20" fill="{t["ink"]}"/>{dots_row(276, 44, 4, 8, 2, "#FFFFFF" if t is THEMES["light"] else "#0D1117", step=.35, dur=2.8, vertical=True)}</g>
  {grid}
  <g>{float_y(-8, 4.5)}<circle cx="470" cy="46" r="9" fill="{t["ink"]}"/></g>
  <g>{float_y(7, 5.5, 1)}<circle cx="690" cy="112" r="13" fill="{t["ink"]}"/></g>
  <path d="M960 112 A44 44 0 0 1 1048 112 Z" fill="{TEAL}"/>
  {dots_row(986, 100, 5, 9, 2, "#FFFFFF", step=.3, dur=2.5)}
  <g>{float_y(-5, 6)}<circle cx="1050" cy="74" r="16" fill="{t["ink"]}"/></g>
  {dots_row(1150, 30, 5, 9, 2.4, TEAL, vertical=True)}{dots_row(1150, 90, 5, 9, 2.4, TEAL, vertical=True)}
  {sparkle(880, 30, .9, SUN, 0)}{sparkle(110, 118, .7, VIOLET, 1.4)}''', "")


# ------------------------------------------------------------------ 2. contour ribbon
def contours(t):
    n, xs = 26, range(120, 1081, 14)
    phases = [0, TAU / 3, 2 * TAU / 3]
    lines = []
    for j in range(n):
        frames = []
        for ph in phases:
            pts = []
            for x in xs:
                u = (x - 120) / 960
                twist = math.sin(u * TAU * .9 + ph) * (j - n / 2) * 3.4      # lines cross over → the ribbon twists
                wave = 18 * math.sin(u * 7 + ph * .5) + 8 * math.sin(u * 15 - ph)
                env = math.sin(math.pi * u) ** .6
                pts.append((x, 75 + env * (wave + twist)))
            frames.append(poly(pts))
        lines.append(morph(frames, 11, f'fill="none" stroke="url(#rg{id(t) % 1000})" stroke-width=".8"'))
    g = f'<defs><linearGradient id="rg{id(t) % 1000}" x1="0" x2="1"><stop offset="0" stop-color="{MINT}"/><stop offset=".45" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CORAL}"/></linearGradient></defs>'
    return svg(g + f'''
  {hatch(30, 30, 46, 90, t["ink"])}
  {hatch(1124, 30, 46, 90, t["ink"])}
  {"".join(lines)}
  <line x1="300" y1="140" x2="420" y2="20" stroke="{t["line"]}" stroke-width="1.2" stroke-dasharray="170" stroke-dashoffset="170"><animate attributeName="stroke-dashoffset" values="170;0;0;-170" keyTimes="0;.3;.7;1" dur="6s" repeatCount="indefinite"/></line>
  <line x1="820" y1="140" x2="960" y2="10" stroke="{t["line"]}" stroke-width="1.2" stroke-dasharray="192" stroke-dashoffset="192"><animate attributeName="stroke-dashoffset" values="192;0;0;-192" keyTimes="0;.3;.7;1" dur="6s" begin="3s" repeatCount="indefinite"/></line>
  <g>{float_y(-10, 6)}<circle cx="600" cy="66" r="30" fill="{CORAL}"><animate attributeName="r" values="30;33;30" dur="3s" repeatCount="indefinite"/></circle></g>
  <g>{float_y(6, 4)}<circle cx="250" cy="44" r="7" fill="{CORAL}"/></g>
  <circle cx="880" cy="118" r="11" fill="{CORAL}"/>
  <circle cx="742" cy="92" r="3" fill="{CORAL}"/>
  <path d="M120 52 A22 22 0 0 0 120 96" fill="none" stroke="{t["ink"]}" stroke-width="7"/>
  <g>{spin(1000, 52, 12)}<path d="M984 58 A18 18 0 0 1 1016 58" fill="none" stroke="{t["ink"]}" stroke-width="7"/></g>
  <path d="M380 112 A14 14 0 0 1 380 140" fill="none" stroke="{t["ink"]}" stroke-width="6"/>
  <g>{spin(474, 42, 9)}<path d="M466 48 L474 34 L482 48 Z" fill="none" stroke="{t["ink"]}" stroke-width="3.5" stroke-linejoin="miter"/></g>
  <g>{spin(1060, 112, 10, True)}<path d="M1050 118 L1060 101 L1070 118 Z" fill="none" stroke="{t["ink"]}" stroke-width="3.5"/></g>
  <g>{spin(203, 118, 8)}{cross(196, 112, 5, t["ink"])}{cross(210, 124, 5, t["ink"])}</g>
  {cross(760, 28, 5, t["ink"])}{cross(774, 28, 5, t["ink"])}{cross(774, 42, 5, t["ink"])}''', "")


# ------------------------------------------------------------------ 3. half-moons, dots and stripes
def moons(t):
    arcs = "".join(f'<path d="M{150 + i * 5} 112 A{50 - i * 5} {50 - i * 5} 0 0 0 {250 - i * 5} 112" fill="none" stroke="#FFFFFF" stroke-width="1.3"/>' for i in range(1, 9))
    arcs2 = "".join(f'<path d="M{846 + i * 4} 40 A{44 - i * 4} {44 - i * 4} 0 0 1 {934 - i * 4} 40" fill="none" stroke="#FFFFFF" stroke-width="1.2"/>' for i in range(1, 8))
    return svg(f'''
  <g><animateTransform attributeName="transform" type="rotate" values="-14 200 112;14 200 112;-14 200 112" dur="7s" repeatCount="indefinite"/>
    <path d="M150 112 A50 50 0 0 0 250 112 Z" fill="{TANGERINE}"/><g>{arcs}</g></g>
  <g>{float_y(-6, 5)}<circle cx="206" cy="96" r="22" fill="{t["ink"]}"/></g>
  {dots_row(300, 74, 22, 12, 2.6, TEAL, step=.12, dur=2.6)}
  <g>{barcode(590, 46, t["ink"], [(4, 5), (4, 5), (10, 5), (4, 5), (16, 5), (4, 0)])}</g>
  <g>{float_y(8, 6, .5)}<circle cx="720" cy="70" r="12" fill="{t["ink"]}"/></g>
  <g><animateTransform attributeName="transform" type="rotate" values="170 890 40;190 890 40;170 890 40" dur="6s" repeatCount="indefinite"/>
    <path d="M846 40 A44 44 0 0 1 934 40 Z" fill="{TEAL}"/>{arcs2}</g>
  {hatch(980, 34, 60, 80, t["ink"], gap=7)}
  {dots_row(1080, 40, 9, 9, 2.4, TEAL, step=.15, dur=2.4, vertical=True)}
  <g>{spin(1130, 108, 14)}<rect x="1122" y="100" width="16" height="16" fill="none" stroke="{CORAL}" stroke-width="3"/></g>
  {sparkle(60, 56, 1, SUN, 0)}{sparkle(520, 120, .7, VIOLET, 1.2)}{sparkle(1160, 40, .8, MINT, 2)}''', "")


for name, fn in (("mesh", mesh), ("contours", contours), ("moons", moons)):
    for theme, t in THEMES.items():
        (HERE / f"divider-{name}-{theme}.svg").write_text(fn(t), encoding="utf-8")
print("dividers ok")
