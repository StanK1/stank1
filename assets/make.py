# Generates the project cards. divider.svg is a static asset; the wireframe cards come from make_wireframes.py. The banner is made by make_banner.py, the design corner by make_creative.py.
import pathlib
OUT = pathlib.Path(__file__).parent
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Ubuntu,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'JetBrains Mono',Menlo,Consolas,monospace"

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

for k, d in CARDS.items():
    (OUT / f"card-{k}.svg").write_text(card(k, d), encoding="utf-8")
print("ok")

print("cards ok")
