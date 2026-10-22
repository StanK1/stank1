# Generates the profile SVGs (dark + light banner, project cards). Re-run after edits.
import pathlib
OUT = pathlib.Path(__file__).parent
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Ubuntu,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'JetBrains Mono',Menlo,Consolas,monospace"

LINES = [
    "I build web apps with React &amp; Next.js",
    "I automate the boring stuff (bank batch jobs included)",
    "I teach AI to read Bulgarian law",
    "I paint on vinyl records 🎨",
]

def banner(theme):
    dark = theme == "dark"
    bg1, bg2 = ("#0B0F19", "#121A2B") if dark else ("#FBFAF7", "#EEF3F1")
    ink = "#E8EDF2" if dark else "#121826"
    muted = "#8A97A8" if dark else "#5C6675"
    accent = "#3DC593" if dark else "#0E7A5A"
    dot = "#1C2638" if dark else "#DCE3E0"
    cycle = 16
    slot = cycle / len(LINES)
    texts = []
    for i, line in enumerate(LINES):
        t0 = i * slot / cycle
        def k(x): return f"{min(max(x, 0), 1):.4f}"
        kt = ["0", k(t0), k(t0 + 1.4 / cycle), k(t0 + (slot - 0.6) / cycle), k(t0 + slot / cycle), "1"]
        # keyTimes must be strictly increasing; collapse duplicates
        vals = ["0", "0", "760", "760", "0", "0"]
        pairs = []
        for a, b in zip(kt, vals):
            if pairs and pairs[-1][0] == a:
                pairs[-1] = (a, b)
            else:
                pairs.append((a, b))
        kts = ";".join(p[0] for p in pairs)
        vs = ";".join(p[1] for p in pairs)
        texts.append(f'''
    <clipPath id="c{i}{theme}"><rect x="96" y="150" height="44" width="0">
      <animate attributeName="width" dur="{cycle}s" repeatCount="indefinite" keyTimes="{kts}" values="{vs}"/>
    </rect></clipPath>
    <text x="100" y="182" clip-path="url(#c{i}{theme})" font-family="{MONO}" font-size="26" fill="{accent}">&gt; {line}</text>''')
    grooves = "".join(f'<circle r="{r}" fill="none" stroke="#2A2A2A" stroke-width="1"/>' for r in range(46, 118, 7))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-label="Hey, I'm Stan — full-stack developer from Sofia">
  <defs>
    <linearGradient id="bg{theme}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/></linearGradient>
    <pattern id="dots{theme}" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.4" fill="{dot}"/></pattern>
    <linearGradient id="paint{theme}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF6B6B"/><stop offset=".35" stop-color="#FFD166"/><stop offset=".65" stop-color="#3DC593"/><stop offset="1" stop-color="#7C6CFF"/></linearGradient>
  </defs>
  <rect width="1200" height="320" rx="24" fill="url(#bg{theme})"/>
  <rect width="1200" height="320" rx="24" fill="url(#dots{theme})" opacity=".7"/>
  <text x="96" y="122" font-family="{FONT}" font-size="64" font-weight="800" fill="{ink}">Hey, I’m Stan <tspan>👋</tspan></text>{''.join(texts)}
  <text x="100" y="250" font-family="{FONT}" font-size="20" fill="{muted}">Full-stack developer · automation engineer · AI tinkerer — Sofia, Bulgaria 🇧🇬</text>
  <g transform="translate(1010 160)">
    <circle r="124" fill="{accent}" opacity=".12"/>
    <g>
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="6s" repeatCount="indefinite"/>
      <circle r="118" fill="#111"/>
      {grooves}
      <path d="M-118 0 A118 118 0 0 1 -40 -111 L-14 -40 A42 42 0 0 0 -42 0 Z" fill="url(#paint{theme})" opacity=".85"/>
      <path d="M60 102 Q 100 40 116 -20" stroke="#FFD166" stroke-width="6" fill="none" stroke-linecap="round" opacity=".9"/>
      <path d="M30 112 Q 80 70 104 10" stroke="#FF6B6B" stroke-width="4" fill="none" stroke-linecap="round" opacity=".8"/>
      <circle r="40" fill="url(#paint{theme})"/>
      <text y="6" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="800" fill="#111">STAN</text>
      <circle r="4" fill="#111"/>
    </g>
  </g>
</svg>'''

CARDS = {
    "lexbg": dict(icon="§", name="LexBG", tag="Bulgarian law for AI assistants",
                  body=["Open-source MCP server: compiles the current", "text of a law from every amendment."],
                  chips=["MCP", "TypeScript", "SQLite"], url="github.com/StanK1/lexbg-mcp",
                  c1="#0E7A5A", c2="#3DC593"),
    "koda": dict(icon="K", name="KODA Studio", tag="Software that gets the job done",
                 body=["AI product studio in Sofia: automating inquiries,", "bookings, orders and reports."],
                 chips=["AI automation", "Integrations", "Dashboards"], url="kodastudio.eu",
                 c1="#5B4BDB", c2="#9B8CFF"),
    "sito": dict(icon="⌂", name="СИТО", tag="Every property listing, once",
                 body=["Property listings from Bulgarian portals,", "deduplicated, in a free daily email."],
                 chips=["Next.js", "Scraping", "Daily digest"], url="sito.homes",
                 c1="#E4572E", c2="#FFB347"),
}

def card(key, d):
    chips, x = [], 28
    for ch in d["chips"]:
        w = 14 + len(ch) * 8.2
        chips.append(f'<rect x="{x}" y="166" width="{w:.0f}" height="28" rx="14" fill="#FFFFFF" fill-opacity=".08" stroke="#FFFFFF" stroke-opacity=".14"/><text x="{x + w/2:.0f}" y="185" text-anchor="middle" font-family="{FONT}" font-size="13" fill="#C9D3DF">{ch}</text>')
        x += w + 8
    body = "".join(f'<text x="28" y="{122 + i*22}" font-family="{FONT}" font-size="15" fill="#A9B4C2">{t}</text>' for i, t in enumerate(d["body"]))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="420" height="236" viewBox="0 0 420 236" role="img" aria-label="{d['name']} — {d['tag']}">
  <defs><linearGradient id="g{key}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{d['c1']}"/><stop offset="1" stop-color="{d['c2']}"/></linearGradient>
    <clipPath id="r{key}"><rect width="420" height="236" rx="20"/></clipPath></defs>
  <g clip-path="url(#r{key})">
    <rect width="420" height="236" fill="#0F1524"/>
    <rect width="420" height="6" fill="url(#g{key})"/>
  </g>
  <rect x=".5" y=".5" width="419" height="235" rx="20" fill="none" stroke="#24304A"/>
  <rect x="28" y="30" width="52" height="52" rx="14" fill="url(#g{key})"/>
  <text x="54" y="66" text-anchor="middle" font-family="{FONT}" font-size="28" font-weight="800" fill="#FFFFFF">{d['icon']}</text>
  <text x="96" y="54" font-family="{FONT}" font-size="22" font-weight="800" fill="#EEF2F6">{d['name']}</text>
  <text x="96" y="76" font-family="{FONT}" font-size="14" fill="{d['c2']}">{d['tag']}</text>
  {body}
  {''.join(chips)}
  <text x="392" y="218" text-anchor="end" font-family="{MONO}" font-size="12" fill="#6E7B8C">{d['url']} ↗</text>
</svg>'''

for t in ("dark", "light"):
    (OUT / f"banner-{t}.svg").write_text(banner(t), encoding="utf-8")
for k, d in CARDS.items():
    (OUT / f"card-{k}.svg").write_text(card(k, d), encoding="utf-8")
print("ok")
