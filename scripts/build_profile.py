"""
Generates the animated SVGs used in the profile README.

Run from the repo root:
    python scripts/build_profile.py

Outputs (written to ./assets):
    dark.svg, light.svg                  hero banner (terminal card)
    pillars-dark.svg, pillars-light.svg  "what I build" cards

Edit the CONFIG block below, re-run, commit the new SVGs.
Animations use SVG SMIL (<animate>), which GitHub renders inside <img>.
No JavaScript, external fonts or external images are used.
"""

from pathlib import Path
from xml.sax.saxutils import escape

# --------------------------------------------------------------------------
# CONFIG: everything personal lives here
# --------------------------------------------------------------------------
CONFIG = {
    "terminal_title": "krishna ~ profile.sh --live",
    "monogram": "K",
    "name": "Krishna",
    "subtitle": "Full-stack developer  /  Discord systems",
    # 2x2 pill grid under the name
    "pills": [
        ("Python · Node · TS", "cyan"),
        ("Discord Systems", "purple"),
        ("Full-Stack Web", "pink"),
        ("Automation & Tools", "green"),
    ],
    "status_label": "BUILDING",
    "status_sub": "bots · automation · web",
    # right-hand "json" panel
    "json_title": "krishna.json",
    "json_rows": [
        ("Name", "Krishna Sharma"),
        ("Handle", "krishna.xyz"),
        ("Role", "Full-stack developer"),
        ("Focus", "Discord systems"),
        ("Languages", "Python · Node.js · TypeScript"),
        ("Stack", "Discord API · REST · Webhooks"),
        ("Tools", "VS Code · Git · Figma"),
    ],
    # pillars section
    "pillars_title": "WHAT I BUILD",
    "pillars": [
        ("Discord Systems", "cyan", [
            "Frameworks · Components V2",
            "Moderation · tickets",
            "Modals · persistent views",
        ]),
        ("Backend & APIs", "purple", [
            "Node.js · Python",
            "REST APIs · webhooks",
            "Real-time data pipelines",
        ]),
        ("Full-Stack Web", "pink", [
            "TypeScript · HTML · CSS",
            "Dashboards · admin panels",
            "Fast, clean front-ends",
        ]),
        ("AI & Tooling", "green", [
            "LLM integrations",
            "CLI tools · scripts",
            "Workflow automation",
        ]),
    ],
}

# --------------------------------------------------------------------------
# THEMES
# --------------------------------------------------------------------------
THEMES = {
    "dark": dict(
        card="#070B16", panel="#0B132B", header="#040711", grid="#1E293B",
        border="#1E293B", text="#F8FAFC", sub="#94A3B8", muted="#64748B",
        leader="#334155", pill_bg="#0A1224",
        cyan="#22D3EE", purple="#A78BFA", pink="#F472B6", green="#10B981",
        pcard="#040711", pcard_bg_top="#0A101F", pcard_bg_bot="#0C1426",
    ),
    "light": dict(
        card="#FFFFFF", panel="#F8FAFC", header="#E2E8F0", grid="#E2E8F0",
        border="#CBD5E1", text="#0F172A", sub="#475569", muted="#64748B",
        leader="#CBD5E1", pill_bg="#F1F5F9",
        cyan="#0891B2", purple="#7C3AED", pink="#BE185D", green="#059669",
        pcard="#F8FAFC", pcard_bg_top="#FFFFFF", pcard_bg_bot="#F1F5F9",
    ),
}

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "'Segoe UI',Inter,Helvetica,Arial,sans-serif"
CHAR_W = 0.6  # monospace glyph width as a fraction of font size


def gradient_defs(t, gid="grad", animated=True):
    """Cyan -> purple -> pink gradient whose colours slowly rotate."""
    c, p, k = t["cyan"], t["purple"], t["pink"]
    def stop(offset, a, b, d):
        if not animated:
            return f'<stop offset="{offset}" stop-color="{a}"/>'
        return (f'<stop offset="{offset}" stop-color="{a}">'
                f'<animate attributeName="stop-color" values="{a};{b};{d};{a}" '
                f'dur="8s" repeatCount="indefinite"/></stop>')
    return (
        f'<linearGradient id="{gid}" x1="0%" y1="0%" x2="100%" y2="0%">'
        f'{stop("0%", c, p, k)}{stop("50%", p, k, c)}{stop("100%", k, c, p)}'
        f'</linearGradient>'
    )


def equalizer(t, x0, baseline, n=16, step=10, bar_w=5, max_h=34):
    """Animated frequency bars (SMIL height + y)."""
    colors = [t["cyan"], t["purple"], t["pink"], t["green"]]
    out = []
    for i in range(n):
        x = x0 + i * step
        color = colors[i % 4]
        dur = round(0.8 + (i % 7) * 0.25, 2)
        lo = 5 + (i * 3) % 9
        hi = max_h - (i * 2) % 12
        out.append(
            f'<rect x="{x}" y="{baseline - lo}" width="{bar_w}" height="{lo}" rx="2" fill="{color}">'
            f'<animate attributeName="height" values="{lo};{hi};{lo}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{baseline - lo};{baseline - hi};{baseline - lo}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.6;1;0.6" dur="{dur}s" repeatCount="indefinite"/>'
            f'</rect>'
        )
    return "\n      ".join(out)


# --------------------------------------------------------------------------
# HERO BANNER
# --------------------------------------------------------------------------
def build_hero(theme_name):
    t = THEMES[theme_name]
    cfg = CONFIG
    W, H = 1180, 420

    # pills (2 x 2)
    pills = []
    px, py, pw, ph, gap = 296, 196, 196, 36, 14
    for i, (label, color) in enumerate(cfg["pills"]):
        x = px + (i % 2) * (pw + gap)
        y = py + (i // 2) * (ph + 12)
        col = t[color]
        pills.append(
            f'<g transform="translate({x},{y})">'
            f'<rect width="{pw}" height="{ph}" rx="{ph // 2}" fill="{t["pill_bg"]}" stroke="{col}" stroke-opacity="0.8"/>'
            f'<text x="{pw // 2}" y="{ph // 2 + 4}" text-anchor="middle" fill="{col}" '
            f'font-size="12.5" font-weight="700" font-family="{SANS}">{escape(label)}</text>'
            f'</g>'
        )
    pills_svg = "\n    ".join(pills)

    # json panel
    jx, jy, jw, jh = 736, 68, 420, 316
    rows = []
    row_y = jy + 82
    for key, val in cfg["json_rows"]:
        kx = jx + 26
        vx = jx + jw - 26
        key_end = kx + len(key) * 13 * CHAR_W + 12
        val_start = vx - len(val) * 13 * CHAR_W - 12
        leader = ""
        if val_start - key_end > 16:
            leader = (f'<line x1="{key_end:.0f}" y1="{row_y - 4}" x2="{val_start:.0f}" y2="{row_y - 4}" '
                      f'stroke="{t["leader"]}" stroke-width="1.5" stroke-dasharray="1 5" stroke-linecap="round"/>')
        rows.append(
            f'<text x="{kx}" y="{row_y}" fill="{t["purple"]}" font-size="13" font-weight="700">{escape(key)}</text>'
            f'{leader}'
            f'<text x="{vx}" y="{row_y}" text-anchor="end" fill="{t["cyan"]}" font-size="13">{escape(val)}</text>'
        )
        row_y += 36
    rows_svg = "\n    ".join(rows)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{MONO}" role="img" aria-label="{escape(cfg["name"])} profile card">
  <defs>
    {gradient_defs(t)}
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="{t["grid"]}" stroke-width="0.5" stroke-opacity="0.5"/>
      <circle cx="40" cy="0" r="1.4" fill="{t["cyan"]}" fill-opacity="0.3"/>
    </pattern>
  </defs>

  <!-- card -->
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="2"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#grid)"/>

  <!-- terminal bar -->
  <path d="M 1 17 C 1 8 8 1 17 1 L {W - 17} 1 C {W - 8} 1 {W - 1} 8 {W - 1} 17 L {W - 1} 44 L 1 44 Z" fill="{t["header"]}"/>
  <circle cx="28" cy="22" r="6" fill="#EF4444"/>
  <circle cx="48" cy="22" r="6" fill="#F59E0B"/>
  <circle cx="68" cy="22" r="6" fill="#10B981"/>
  <text x="{W // 2}" y="27" text-anchor="middle" fill="{t["sub"]}" font-size="13" font-weight="600">{escape(cfg["terminal_title"])}</text>
  <line x1="1" y1="44" x2="{W - 1}" y2="44" stroke="{t["border"]}"/>

  <!-- monogram avatar -->
  <g>
    <circle cx="150" cy="238" r="108" fill="none" stroke="url(#grad)" stroke-width="3" stroke-dasharray="12 9">
      <animateTransform attributeName="transform" type="rotate" from="0 150 238" to="360 150 238" dur="22s" repeatCount="indefinite"/>
    </circle>
    <circle cx="150" cy="238" r="100" fill="none" stroke="{t["cyan"]}" stroke-width="1.5">
      <animate attributeName="stroke-opacity" values="0.8;0.2;0.8" dur="3s" repeatCount="indefinite"/>
    </circle>
    <circle cx="150" cy="238" r="92" fill="{t["panel"]}" stroke="{t["border"]}" stroke-width="2"/>
    <text x="150" y="272" text-anchor="middle" fill="url(#grad)" font-size="96" font-weight="800" font-family="{SANS}">{escape(cfg["monogram"])}</text>
  </g>

  <!-- identity -->
  <text x="296" y="128" fill="url(#grad)" font-size="48" font-weight="800" font-family="{SANS}">{escape(cfg["name"])}</text>
  <text x="298" y="160" fill="{t["sub"]}" font-size="14">{escape(cfg["subtitle"])}</text>

  {pills_svg}

  <!-- status pill + equalizer -->
  <g transform="translate(296,292)">
    <rect width="406" height="78" rx="14" fill="{t["panel"]}" stroke="{t["border"]}"/>
    <circle cx="26" cy="39" r="6" fill="{t["green"]}">
      <animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/>
    </circle>
    <text x="44" y="35" fill="{t["text"]}" font-size="13" font-weight="700" font-family="{SANS}">STATUS: <tspan fill="{t["green"]}">{escape(cfg["status_label"])}</tspan></text>
    <text x="44" y="55" fill="{t["muted"]}" font-size="11">{escape(cfg["status_sub"])}</text>
    <rect x="224" y="12" width="168" height="54" rx="10" fill="{t["card"]}" stroke="{t["border"]}"/>
    <g>
      {equalizer(t, x0=236, baseline=58, n=16, step=10, bar_w=5, max_h=34)}
    </g>
  </g>

  <!-- json panel -->
  <rect x="{jx}" y="{jy}" width="{jw}" height="{jh}" rx="14" fill="{t["header"]}" fill-opacity="0.55" stroke="{t["border"]}" stroke-width="1.5"/>
  <text x="{jx + jw // 2}" y="{jy + 28}" text-anchor="middle" fill="{t["sub"]}" font-size="12" font-weight="600">{escape(cfg["json_title"])}</text>
  <line x1="{jx}" y1="{jy + 42}" x2="{jx + jw}" y2="{jy + 42}" stroke="{t["border"]}"/>
  {rows_svg}
</svg>
'''
    return svg


# --------------------------------------------------------------------------
# PILLARS
# --------------------------------------------------------------------------
def build_pillars(theme_name):
    t = THEMES[theme_name]
    cfg = CONFIG
    W, H = 1180, 226
    cw, ch, gap = 260, 122, 20
    x0, y0 = 40, 80

    cards = []
    for i, (title, color, lines) in enumerate(cfg["pillars"]):
        col = t[color]
        x = x0 + i * (cw + gap)
        begin = f"{i * 0.6:.1f}s"
        text_lines = []
        for j, line in enumerate(lines):
            fill = t["text"] if j == 0 else t["sub"]
            text_lines.append(
                f'<text x="22" y="{58 + j * 22}" fill="{fill}" font-size="12">{escape(line)}</text>'
            )
        cards.append(
            f'<g transform="translate({x},{y0})">'
            f'<rect width="{cw}" height="{ch}" rx="12" fill="{t["pcard"]}" stroke="{col}" stroke-opacity="0.85">'
            f'<animate attributeName="stroke-opacity" values="0.85;0.3;0.85" dur="4s" begin="{begin}" repeatCount="indefinite"/>'
            f'</rect>'
            f'<rect x="0" y="18" width="4" height="22" rx="2" fill="{col}"/>'
            f'<text x="22" y="34" fill="{col}" font-size="15" font-weight="700" font-family="{SANS}">{escape(title)}</text>'
            + "".join(text_lines) +
            f'</g>'
        )
    cards_svg = "\n  ".join(cards)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{MONO}" role="img" aria-label="{escape(cfg["pillars_title"])}">
  <defs>
    {gradient_defs(t, "pgrad", animated=False)}
    <linearGradient id="pbg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t["pcard_bg_top"]}"/>
      <stop offset="1" stop-color="{t["pcard_bg_bot"]}"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#pbg)" stroke="{t["border"]}" stroke-width="2"/>
  <text x="40" y="44" fill="url(#pgrad)" font-size="20" font-weight="800" font-family="{SANS}" letter-spacing="1.5">{escape(cfg["pillars_title"])}</text>
  <line x1="40" y1="58" x2="{W - 40}" y2="58" stroke="{t["border"]}"/>
  {cards_svg}
</svg>
'''
    return svg


# --------------------------------------------------------------------------
def main():
    out = Path(__file__).resolve().parent.parent / "assets"
    out.mkdir(exist_ok=True)
    for name in ("dark", "light"):
        (out / f"{name}.svg").write_text(build_hero(name), encoding="utf-8")
        (out / f"pillars-{name}.svg").write_text(build_pillars(name), encoding="utf-8")
    print("wrote:", *sorted(p.name for p in out.glob("*.svg")))


if __name__ == "__main__":
    main()
