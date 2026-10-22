"""Animated 'creative ideas' illustration for the profile README.
Shapes are taken from Creative_Ideas_Illustration.svg (assets/src) and given motion:
gears turn, the bulb lights up, the circles float, the letters pop in, the skills appear one by one.
Run: python3 assets/make_creative.py  →  assets/creative.svg
"""
import pathlib, re

HERE = pathlib.Path(__file__).parent
SRC = (HERE / "src" / "Creative_Ideas_Illustration.svg").read_text(encoding="utf-8")
items = re.findall(r'<(path|circle)\s+style="fill:(#[0-9A-Fa-f]{6});"\s*([^>]*?)/>', SRC, re.S)
shape = [f'<{t} {re.sub(r"\s+", " ", a).strip()}' for t, f, a in items]
fills = [f for t, f, a in items]

def el(i, fill=None, extra=""):
    return f'{shape[i]} fill="{fill or fills[i]}" {extra}/>'

def el_anim(i, inner, fill=None):
    tag = items[i][0]
    return f'{shape[i]} fill="{fill or fills[i]}">{inner}</{tag}>'

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Ubuntu,Helvetica,Arial,sans-serif"
MINT, VIOLET, TANGERINE, SUN, CORAL, INK = "#3DC593", "#7C6CFF", "#FF8A3D", "#FFD166", "#FF6B6B", "#0B0F19"
CYCLE = 6  # seconds: letters pop → bulb lights up → rest

# --- gears (centres from the source geometry) -------------------------------------------
gear_small = "".join(el(i) for i in (0, 1, 2))
gear_big = "".join(el(i) for i in (3, 4, 5))
gears = f'''
  <g><animateTransform attributeName="transform" type="rotate" from="0 652.6 673.2" to="360 652.6 673.2" dur="16s" repeatCount="indefinite"/>{gear_big}</g>
  <g><animateTransform attributeName="transform" type="rotate" from="0 743.289 840.778" to="-360 743.289 840.778" dur="8s" repeatCount="indefinite"/>{gear_small}</g>'''

# --- bulb: glass lights up, filament glows, rays burst --------------------------------
on = "0;.45;.55;.9;1"
glass = el_anim(6, f'<animate attributeName="fill" values="#CCCCCC;#CCCCCC;#FFE08A;#FFE08A;#CCCCCC" keyTimes="{on}" dur="{CYCLE}s" repeatCount="indefinite"/>')
fil = "".join(el_anim(i, f'<animate attributeName="fill" values="#1A1A1E;#1A1A1E;{TANGERINE};{TANGERINE};#1A1A1E" keyTimes="{on}" dur="{CYCLE}s" repeatCount="indefinite"/>') for i in (9, 10))
base = "".join(el(i) for i in (8, 11, 12, 13))
rays = []
cx, cy = 500.6, 627.5
import math
for k in range(9):
    a = math.radians(-180 + k * 22.5)
    x1, y1 = cx + math.cos(a) * 168, cy + math.sin(a) * 168
    x2, y2 = cx + math.cos(a) * 212, cy + math.sin(a) * 212
    rays.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{SUN}" stroke-width="12" stroke-linecap="round"/>')
bulb = f'''
  <circle cx="{cx}" cy="{cy}" r="170" fill="{SUN}" opacity="0"><animate attributeName="opacity" values="0;0;.45;.3;0" keyTimes="{on}" dur="{CYCLE}s" repeatCount="indefinite"/></circle>
  <g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{on}" dur="{CYCLE}s" repeatCount="indefinite"/>
    <g><animateTransform attributeName="transform" type="scale" values="1;1;1.08;1;1" keyTimes="{on}" dur="{CYCLE}s" repeatCount="indefinite" additive="sum"/>{''.join(rays)}</g>
  </g>
  {glass}{el(7)}{base}{fil}'''

# --- circles with their words, floating ---------------------------------------------------
inspiration = el(17, MINT) + "".join(el(i) for i in range(28, 39))
ideas = el(18, VIOLET) + "".join(el(i) for i in range(39, 44))
float_a = f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -16;0 0" dur="5s" repeatCount="indefinite"/>'
float_b = f'<animateTransform attributeName="transform" type="translate" values="0 0;0 14;0 0" dur="6s" repeatCount="indefinite"/>'
orange = f'''<g><animateTransform attributeName="transform" type="scale" values="1;1.025;1" dur="4s" repeatCount="indefinite" additive="sum"/>
    {el(19, TANGERINE, 'style="transform-origin:623.9px 483.1px"')}</g>'''.replace('<animateTransform attributeName="transform" type="scale" values="1;1.025;1" dur="4s" repeatCount="indefinite" additive="sum"/>', '')
orange = f'{el(19, TANGERINE)}'
orange_pulse = f'<circle cx="623.941" cy="483.112" r="269.238" fill="none" stroke="{TANGERINE}" stroke-width="3" opacity=".6"><animate attributeName="r" values="269;300;269" dur="4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".6;0;.6" dur="4s" repeatCount="indefinite"/></circle>'

# --- CREATIVE letters pop in, one after another -------------------------------------------
letters = []
for n, i in enumerate(range(20, 28)):
    t0 = 0.04 + n * 0.035
    kt = f"0;{t0:.3f};{t0 + .06:.3f};{t0 + .1:.3f};.92;1"
    letters.append(f'''<g><animateTransform attributeName="transform" type="translate" values="0 40;0 40;0 -10;0 0;0 0;0 40" keyTimes="{kt}" dur="{CYCLE}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0;1;1;1;0" keyTimes="{kt}" dur="{CYCLE}s" repeatCount="indefinite"/>{el(i, INK)}</g>''')

# --- sparkles -----------------------------------------------------------------------------
def sparkle(x, y, s, col, d):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M0 -14 L3.5 -3.5 L14 0 L3.5 3.5 L0 14 L-3.5 3.5 L-14 0 L-3.5 -3.5 Z" fill="{col}"><animate attributeName="opacity" values="0;1;0" dur="2.6s" begin="{d}s" repeatCount="indefinite"/></path></g>'
sparkles = sparkle(200, 420, 1.2, SUN, 0) + sparkle(980, 300, 1, VIOLET, .8) + sparkle(380, 880, .9, CORAL, 1.6) + sparkle(1000, 900, 1.1, MINT, 2.2) + sparkle(860, 250, .7, TANGERINE, 1.2)

# --- right panel: headline + skills appearing one by one ---------------------------------
skills = [("UX / UI", MINT), ("Design systems", VIOLET), ("Figma", CORAL), ("Photoshop", "#31A8FF"), ("Illustrator", "#FF9A00"),
          ("InDesign", "#FF3366"), ("After Effects", "#9999FF"), ("Premiere Pro", "#9999FF"), ("Blender", "#F5792A")]
chips, x, y = [], 0, 0
for n, (name, col) in enumerate(skills):
    w = 46 + len(name) * 13
    if x + w > 450:
        x, y = 0, y + 62
    d = n * 0.25
    chips.append(f'''<g transform="translate({x} {y})" opacity="0"><animate attributeName="opacity" values="0;1" dur=".4s" begin="{d}s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate" values="{x} {y + 16};{x} {y}" dur=".4s" begin="{d}s" fill="freeze"/>
      <rect width="{w}" height="46" rx="23" fill="#FFFFFF" stroke="{col}" stroke-width="3"/>
      <circle cx="22" cy="23" r="7" fill="{col}"/>
      <text x="38" y="30" font-family="{FONT}" font-size="20" font-weight="600" fill="{INK}">{name}</text></g>''')
    x += w + 12
panel = f'''
  <g transform="translate(1100 150)">
    <text font-family="{FONT}" font-size="24" font-weight="700" fill="{TANGERINE}">Design corner</text>
    <text y="62" font-family="{FONT}" font-size="50" font-weight="800" fill="{INK}">Where ideas</text>
    <text y="122" font-family="{FONT}" font-size="50" font-weight="800" fill="{INK}">get made.</text>
    <path d="M2 140 C 80 128, 160 150, 250 134" fill="none" stroke="{TANGERINE}" stroke-width="7" stroke-linecap="round" stroke-dasharray="270" stroke-dashoffset="270">
      <animate attributeName="stroke-dashoffset" values="270;0;0;270" keyTimes="0;.2;.9;1" dur="{CYCLE}s" repeatCount="indefinite"/></path>
    <text y="196" font-family="{FONT}" font-size="22" fill="#4A5363">Interfaces, design systems, motion and 3D.</text>
    <g transform="translate(0 236)">{''.join(chips)}</g>
  </g>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="760" viewBox="0 0 1600 760" role="img" aria-label="Creative ideas: a lightbulb switching on, turning gears and floating circles labelled Inspiration and Ideas, next to design skills">
  <defs>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.6" fill="#E9DFD0"/></pattern>
  </defs>
  <rect width="1600" height="760" rx="32" fill="#FFF8EF"/>
  <rect width="1600" height="760" rx="32" fill="url(#grid)"/>
  <g transform="translate(10 -175)">
    {orange_pulse}{orange}
    {gears}
    {bulb}
    <g>{float_a}{inspiration}</g>
    <g>{float_b}{ideas}</g>
    {''.join(letters)}
    {sparkles}
  </g>
  {panel}
</svg>'''
(HERE / "creative.svg").write_text(svg, encoding="utf-8")
print("ok", len(svg))
