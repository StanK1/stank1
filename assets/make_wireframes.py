"""Two animated section backgrounds made from the original wireframe illustrations in assets/src.
The artwork is used as drawn; each piece gets its own motion:
  wireframe-a.svg  (Wireframe_A.svg)  swirl lines draw themselves, balls float, dots blink, mesh sways
  wireframe-b.svg  (Wireframe_B.svg)  the wave lines draw in, crosses and arcs turn, circles float, rules slide
Run: python3 assets/make_wireframes.py
"""
import pathlib, re
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).parent
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
q = lambda tag: f"{{{NS}}}{tag}"

CARD_W = 1200
PAPER, DOT = "#FFFFFF", "#EEEAF2"   # white: the original swirls are white lines meant to sit on white


def anim(parent, tag, **attrs):
    a = ET.SubElement(parent, q(tag))
    for k, v in attrs.items():
        a.set(k.replace("_", "-") if k not in ("from_",) else "from", str(v))
    return a


def wrap(objects, i):
    """Put child i of OBJECTS inside a new <g> (so its motion never fights its own transform)."""
    child = list(objects)[i]
    idx = list(objects).index(child)
    g = ET.Element(q("g"))
    objects.remove(child)
    g.append(child)
    objects.insert(idx, g)
    return g


def float_(g, dy, dur, begin=0):
    anim(g, "animateTransform", attributeName="transform", type="translate", values=f"0 0;0 {dy};0 0",
         dur=f"{dur}s", begin=f"{begin}s", repeatCount="indefinite", additive="sum")


def sway(g, dx, dy, dur):
    anim(g, "animateTransform", attributeName="transform", type="translate", values=f"0 0;{dx} {dy};0 0;{-dx} {-dy};0 0",
         dur=f"{dur}s", repeatCount="indefinite", additive="sum")


def turn(g, cx, cy, deg, dur, rock=False):
    vals = f"{-deg} {cx} {cy};{deg} {cx} {cy};{-deg} {cx} {cy}" if rock else f"0 {cx} {cy};{deg} {cx} {cy}"
    anim(g, "animateTransform", attributeName="transform", type="rotate", values=vals, dur=f"{dur}s",
         repeatCount="indefinite", additive="sum")


def pulse(g, cx, cy, s, dur):
    # scale around (cx, cy): translate → scale → translate back, expressed as a matrix-free trick
    anim(g, "animateTransform", attributeName="transform", type="translate",
         values=f"0 0;{cx * (1 - s):.2f} {cy * (1 - s):.2f};0 0", dur=f"{dur}s", repeatCount="indefinite", additive="sum")
    anim(g, "animateTransform", attributeName="transform", type="scale", values=f"1;{s};1", dur=f"{dur}s",
         repeatCount="indefinite", additive="sum")


def draw_lines(g, dur, stagger, hold=.55):
    """Stroked paths and lines draw themselves, hold, then undraw — staggered one after another."""
    strokes = [e for e in g.iter() if e.tag in (q("path"), q("line"), q("polyline"))
               and ("stroke" in (e.get("style") or "") or e.tag == q("line"))]
    for n, e in enumerate(strokes):
        e.set("pathLength", "1")
        e.set("stroke-dasharray", "1")
        e.set("stroke-dashoffset", "1")
        anim(e, "animate", attributeName="stroke-dashoffset", values="1;0;0;-1",
             keyTimes=f"0;.3;{.3 + hold:.2f};1", dur=f"{dur}s", begin=f"{n * stagger:.2f}s", repeatCount="indefinite")
    return len(strokes)


def blink(g, step, dur, only=None):
    dots = [e for e in g.iter() if e.tag == q("circle") and (not only or only in (e.get("style") or "").upper())]
    for n, e in enumerate(dots):
        anim(e, "animate", attributeName="opacity", values="1;.25;1", dur=f"{dur}s", begin=f"{n * step:.2f}s",
             repeatCount="indefinite")
    return len(dots)


def load(name):
    root = ET.parse(HERE / "src" / name).getroot()
    for g in list(root):
        if g.get("id") == "BACKGROUND":
            root.remove(g)
    objects = next(g for g in root if g.get("id") == "OBJECTS")
    return root, objects


def card(root, vb, label):
    """The artwork cropped to vb (in its own units), scaled to CARD_W wide, on a white rounded card."""
    x, y, w, h = vb
    s = CARD_W / w
    H = round(h * s)
    inner = "".join(ET.tostring(c, encoding="unicode") for c in root)
    inner = re.sub(r'\sxmlns(:\w+)?="[^"]+"', "", inner)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{CARD_W}" height="{H}" viewBox="0 0 {CARD_W} {H}" role="img" aria-label="{label}">
  <defs>
    <pattern id="paper-grid" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.6" fill="{DOT}"/></pattern>
    <clipPath id="card-clip"><rect width="{CARD_W}" height="{H}" rx="36"/></clipPath>
  </defs>
  <rect width="{CARD_W}" height="{H}" rx="36" fill="{PAPER}"/>
  <rect width="{CARD_W}" height="{H}" rx="36" fill="url(#paper-grid)"/>
  <g clip-path="url(#card-clip)"><g transform="scale({s:.4f}) translate({-x} {-y})">{inner}</g></g>
</svg>'''


# ------------------------------------------------------------------ A
root, obj = load("Wireframe_A.svg")
# indices are positions inside OBJECTS (see the README of this script / bounding boxes):
# 0 orange disc + half-disc, 1 white swirl lines, 2-5 black balls, 6 black circles with dot columns,
# 7 wireframe meshes, 8 barcode, 9 teal dot rows, 10 teal dot columns, brush stroke and the rest
groups = {i: wrap(obj, i) for i in range(len(list(obj)))}
pulse(groups[0], 228, 178, 1.03, 5)
draw_lines(groups[1], 7, .05)
float_(groups[2], -10, 4.5)
float_(groups[3], 8, 5, .6)
float_(groups[4], -7, 3.8, 1.1)
float_(groups[5], 9, 6, .3)
blink(groups[6], .18, 2.4, only="#FFFFFF")
sway(groups[7], 6, 4, 10)
for n, r in enumerate(e for e in groups[8].iter() if e.tag == q("rect")):
    anim(r, "animate", attributeName="opacity", values="1;.35;1", dur="2.6s", begin=f"{n * .15:.2f}s", repeatCount="indefinite")
blink(groups[9], .08, 2.2)
blink(groups[10], .06, 2.6)
(HERE / "wireframe-a.svg").write_text(card(root, (0, 10, 750, 470), "Abstract wireframe illustration with an orange disc, floating black circles and a rippling mesh"), encoding="utf-8")

# ------------------------------------------------------------------ B
root, obj = load("Wireframe_B.svg")
groups = {i: wrap(obj, i) for i in range(len(list(obj)))}
centres = {0: (193, 110), 1: (204, 121), 2: (536, 385), 3: (549, 385), 4: (549, 399)}
for i, (cx, cy) in centres.items():                                   # crosses spin
    turn(groups[i], cx, cy, 360 if i % 2 else -360, 6 + i)
pulse(groups[5], 415.5, 173.5, 1.08, 4)                                # big circle breathes
float_(groups[5], -8, 6)
draw_lines(groups[6], 9, .025, hold=.5)                                # the wave draws itself
sway(groups[6], 0, 5, 8)
float_(groups[7], 10, 7)                                               # hatching slides
float_(groups[8], -10, 7, 1)
for i, (cx, cy), deg, d in ((9, (530, 128), 25, 5), (10, (153, 360), 30, 6), (11, (71, 170), 20, 7)):
    turn(groups[i], cx, cy, deg, d, rock=True)                         # arcs rock
turn(groups[12], 279, 193, 360, 9)                                     # triangles turn
turn(groups[13], 615, 308, -360, 11)
for i, dy, d, b in ((14, -12, 5, 0), (15, 8, 4, .4), (16, -9, 4.6, 1), (17, 6, 3, .2)):
    float_(groups[i], dy, d, b)
for n, i in enumerate((18, 19, 20, 21)):
    draw_lines(groups[i], 6, 0)
    for a in groups[i].iter(q("animate")):
        a.set("begin", f"{n * 1.2:.1f}s")
(HERE / "wireframe-b.svg").write_text(card(root, (20, 80, 710, 370), "Abstract wireframe illustration: a wave of fine lines with red circles, rings, triangles and crosses"), encoding="utf-8")
print("wireframes ok")
