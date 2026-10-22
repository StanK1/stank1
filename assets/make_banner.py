"""Animated header banner for the profile README, in the same illustrated style as creative.svg.
Left: name, a pen-tool curve that draws itself under it, and lines that type out one by one.
Right: the bulb, gears and floating circles from Creative_Ideas_Illustration.svg (assets/src).
Run: python3 assets/make_banner.py  →  assets/banner-light.svg, assets/banner-dark.svg
"""
import math, pathlib, re

HERE = pathlib.Path(__file__).parent
SRC = (HERE / "src" / "Creative_Ideas_Illustration.svg").read_text(encoding="utf-8")
items = re.findall(r'<(path|circle)\s+style="fill:(#[0-9A-Fa-f]{6});"\s*([^>]*?)/>', SRC, re.S)
shape = [f'<{t} {re.sub(r"\s+", " ", a).strip()}' for t, f, a in items]
fills = [f for t, f, a in items]

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Ubuntu,Helvetica,Arial,sans-serif"
MINT, VIOLET, TANGERINE, SUN, CORAL = "#3DC593", "#7C6CFF", "#FF8A3D", "#FFD166", "#FF6B6B"
W, H = 1400, 440

THEMES = {
    "light": dict(paper="#FFF8EF", dot="#E9DFD0", ink="#1B1726", muted="#6B6478", handle="#B9AFC6",
                  recolor={}),
    # dark gear and base parts would vanish on a dark background, so they are lifted
    "dark": dict(paper="#17141F", dot="#2C2738", ink="#F3EEF8", muted="#A39CB3", handle="#5E5670",
                 recolor={"#1A1A1E": "#E6E0EE", "#767676": "#9C95AE"}),
}

LINES = [
    "I design interfaces and design systems",
    "I build web apps with React and Next.js",
    "I run KODA Studio and build СИТО",
    "I teach AI to read Bulgarian law",
    "Off screen, I make art",
]
SLOT = 3.6                      # seconds per line
CYCLE = SLOT * len(LINES)
TYPE_SIZE = 32
X0, TYPE_Y = 100, 268


def el(i, t, fill=None, inner=None):
    f = fill or t["recolor"].get(fills[i], fills[i])
    if inner is None:
        return f'{shape[i]} fill="{f}"/>'
    return f'{shape[i]} fill="{f}">{inner}</{items[i][0]}>'


def k(x):
    return f"{min(max(x, 0), 1):.4f}"


def typing(t, theme):
    out = []
    for n, line in enumerate(LINES):
        w = round(len(line) * TYPE_SIZE * 0.49) + 4           # approximate rendered width
        a = n * SLOT / CYCLE
        typed = a + (0.25 + len(line) * 0.035) / CYCLE        # type speed ~35 ms per character
        hold = a + (SLOT - 0.45) / CYCLE
        gone = a + SLOT / CYCLE
        kts, wv, cx = ["0"], ["0"], [str(X0)]
        for kt, v in ((a, 0), (typed, w), (hold, w), (gone, 0)):
            if k(kt) != kts[-1]:
                kts.append(k(kt)); wv.append(str(v)); cx.append(str(X0 + v + 4))
        if kts[-1] != "1.0000":
            kts.append("1"); wv.append("0"); cx.append(str(X0))
        vis = ";".join("1" if a <= float(x) < gone else "0" for x in kts)
        out.append(f'''
    <clipPath id="ln{n}{theme}"><rect x="{X0 - 4}" y="{TYPE_Y - 34}" height="48" width="0">
      <animate attributeName="width" dur="{CYCLE}s" repeatCount="indefinite" keyTimes="{';'.join(kts)}" values="{';'.join(wv)}"/></rect></clipPath>
    <text x="{X0}" y="{TYPE_Y}" clip-path="url(#ln{n}{theme})" font-family="{FONT}" font-size="{TYPE_SIZE}" font-weight="500" fill="{t['ink']}">{line}</text>
    <rect y="{TYPE_Y - 28}" width="3" height="36" rx="1.5" fill="{TANGERINE}" opacity="0">
      <animate attributeName="x" dur="{CYCLE}s" repeatCount="indefinite" keyTimes="{';'.join(kts)}" values="{';'.join(cx)}"/>
      <animate attributeName="opacity" dur="{CYCLE}s" repeatCount="indefinite" keyTimes="{';'.join(kts)}" values="{vis}" calcMode="discrete"/></rect>''')
    return "".join(out)


def pen(t):
    """A Bezier drawn with the pen tool: the stroke grows, handles and anchors appear, then rest."""
    d = "M104 186 C 220 214, 330 150, 450 178 S 610 206, 648 170"
    draw = "2.2s"
    anchors = [(104, 186), (450, 178), (648, 170)]
    handles = [((450, 178), (330, 150)), ((450, 178), (570, 206))]
    hs = "".join(f'''<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{t['handle']}" stroke-width="2"/>
      <circle cx="{b[0]}" cy="{b[1]}" r="6" fill="{t['paper']}" stroke="{t['handle']}" stroke-width="2"/>''' for a, b in handles)
    an = "".join(f'<rect x="{x - 7}" y="{y - 7}" width="14" height="14" fill="{t["paper"]}" stroke="{VIOLET}" stroke-width="3"/>' for x, y in anchors)
    return f'''
  <path d="{d}" fill="none" stroke="{VIOLET}" stroke-width="6" stroke-linecap="round" stroke-dasharray="600" stroke-dashoffset="600">
    <animate attributeName="stroke-dashoffset" from="600" to="0" dur="{draw}" begin=".3s" fill="freeze" calcMode="spline" keySplines=".6 0 .3 1" keyTimes="0;1"/></path>
  <g opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.7;1" dur="3s" begin="1.2s" fill="freeze"/>{hs}</g>
  <g opacity="0"><animate attributeName="opacity" to="1" dur=".3s" begin="1.6s" fill="freeze"/>{an}</g>
  <g opacity="0">
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="{draw}" begin=".3s" fill="freeze"/>
    <animateMotion path="{d}" dur="{draw}" begin=".3s" fill="freeze" calcMode="spline" keySplines=".6 0 .3 1" keyTimes="0;1"/>
    <path transform="translate(-2 -34)" d="M2 34 L8 14 L18 4 L28 14 L18 24 Z" fill="{t['ink']}"/>
    <circle cx="13" cy="19" r="2.6" fill="{t['paper']}" transform="translate(-2 -34)"/></g>'''


def illustration(t):
    cyc = 6
    on = "0;.45;.55;.9;1"
    gear_big = "".join(el(i, t) for i in (3, 4, 5))
    gear_small = "".join(el(i, t) for i in (0, 1, 2))
    gears = f'''
    <g><animateTransform attributeName="transform" type="rotate" from="0 652.6 673.2" to="360 652.6 673.2" dur="16s" repeatCount="indefinite"/>{gear_big}</g>
    <g><animateTransform attributeName="transform" type="rotate" from="0 743.289 840.778" to="-360 743.289 840.778" dur="8s" repeatCount="indefinite"/>{gear_small}</g>'''
    glass = el(6, t, "#CCCCCC", f'<animate attributeName="fill" values="#CCCCCC;#CCCCCC;#FFE08A;#FFE08A;#CCCCCC" keyTimes="{on}" dur="{cyc}s" repeatCount="indefinite"/>')
    fil = "".join(el(i, t, "#1A1A1E", f'<animate attributeName="fill" values="#1A1A1E;#1A1A1E;{TANGERINE};{TANGERINE};#1A1A1E" keyTimes="{on}" dur="{cyc}s" repeatCount="indefinite"/>') for i in (9, 10))
    base = "".join(el(i, t) for i in (8, 11, 12, 13))
    cx, cy = 500.6, 627.5
    rays = "".join(
        f'<line x1="{cx + math.cos(a) * 168:.1f}" y1="{cy + math.sin(a) * 168:.1f}" x2="{cx + math.cos(a) * 212:.1f}" y2="{cy + math.sin(a) * 212:.1f}" stroke="{SUN}" stroke-width="12" stroke-linecap="round"/>'
        for a in (math.radians(-180 + n * 22.5) for n in range(9)))
    bulb = f'''
    <circle cx="{cx}" cy="{cy}" r="170" fill="{SUN}" opacity="0"><animate attributeName="opacity" values="0;0;.45;.3;0" keyTimes="{on}" dur="{cyc}s" repeatCount="indefinite"/></circle>
    <g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{on}" dur="{cyc}s" repeatCount="indefinite"/>{rays}</g>
    {glass}{el(7, t)}{base}{fil}'''
    inspiration = el(17, t, MINT) + "".join(el(i, t, "#FFFFFF") for i in range(28, 39))
    ideas = el(18, t, VIOLET) + "".join(el(i, t, "#FFFFFF") for i in range(39, 44))
    pulse = f'<circle cx="623.941" cy="483.112" r="269.238" fill="none" stroke="{TANGERINE}" stroke-width="4" opacity=".6"><animate attributeName="r" values="269;305;269" dur="4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".6;0;.6" dur="4s" repeatCount="indefinite"/></circle>'
    return f'''
  <g transform="translate(800 -88) scale(.55)">
    {pulse}{el(19, t, TANGERINE)}
    {gears}
    {bulb}
    <g><animateTransform attributeName="transform" type="translate" values="0 0;0 -18;0 0" dur="5s" repeatCount="indefinite"/>{inspiration}</g>
    <g><animateTransform attributeName="transform" type="translate" values="0 0;0 16;0 0" dur="6s" repeatCount="indefinite"/>{ideas}</g>
  </g>'''


def sparkle(x, y, s, col, d):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 -14 L3.5 -3.5 L14 0 L3.5 3.5 L0 14 L-3.5 3.5 L-14 0 L-3.5 -3.5 Z" fill="{col}">'
            f'<animate attributeName="opacity" values="0;1;0" dur="2.6s" begin="{d}s" repeatCount="indefinite"/></path></g>')


def banner(theme):
    t = THEMES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Hi, I'm Stan. Developer, designer and founder from Sofia, Bulgaria.">
  <defs><pattern id="grid{theme}" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.6" fill="{t['dot']}"/></pattern></defs>
  <rect width="{W}" height="{H}" rx="32" fill="{t['paper']}"/>
  <rect width="{W}" height="{H}" rx="32" fill="url(#grid{theme})"/>
  <text x="{X0 - 6}" y="152" font-family="{FONT}" font-size="104" font-weight="800" letter-spacing="-3" fill="{t['ink']}">Hi, I’m Stan</text>
  {pen(t)}
  {typing(t, theme)}
  <text x="{X0}" y="352" font-family="{FONT}" font-size="24" fill="{t['muted']}">Developer, designer and founder in Sofia, Bulgaria</text>
  {illustration(t)}
  {sparkle(770, 70, 1.1, SUN, 0)}{sparkle(800, 380, .8, CORAL, 1.3)}{sparkle(1370, 60, .9, MINT, .7)}{sparkle(1352, 404, .7, VIOLET, 2)}
</svg>'''


for theme in THEMES:
    (HERE / f"banner-{theme}.svg").write_text(banner(theme), encoding="utf-8")
print("banners ok")
