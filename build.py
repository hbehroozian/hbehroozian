"""Generate the SVG graphics for the GitHub profile README into assets/.

    python build.py

Logos come from brand/ (copied from the Dev Fusion Lab, Panjera and Jeeraph
repos) and are embedded as data URIs, because GitHub shows README images as
<img>, which cannot load other files.
"""

import base64
import re
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
ASSETS = HERE / "assets"

SERIF = "Georgia, 'Times New Roman', serif"
SANS = "Inter, -apple-system, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'IBM Plex Mono', ui-monospace, 'SF Mono', 'Cascadia Mono', Consolas, Menlo, monospace"

# The Dev Fusion Lab site's ground (near-black page, panels one step lighter,
# white text with two greys, hairlines in white at low opacity) with the
# avatar's amber as the one accent: labels, glows, the underline, the buttons.
# Edges are square with notched corners. Panjera and Jeeraph keep their own palettes.
INK = "#08090a"        # page / header
PANEL = "#0f1011"      # cards
SHADOW = "#502828"     # the avatar's maroon, for pixel drop shadows
CREAM = "#f7f8f8"      # primary text (name kept for the older call sites)
PALE = "#ffd888"       # highlight
MUTED = "#a1a5ad"
FAINT = "#8a8f98"
AMBER = "#ffa000"      # the accent
ORANGE = "#f08050"
BUTTON_INK = "#2a1416" # text and marks on the amber buttons
GREEN = AMBER          # older call sites
LINE = "rgba(255,255,255,0.10)"
PX = 4                 # the pixel unit

REDUCED_MOTION = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def data_uri(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def logo(name: str) -> str:
    return (HERE / "brand" / name).read_text(encoding="utf-8")


AVATAR = "data:image/png;base64," + base64.b64encode((HERE / "brand" / "avatar-256.png").read_bytes()).decode()
DFL_MARK = data_uri(logo("devfusionlab-mark.svg").replace("currentColor", "#ffffff"))
DFL_MARK_DARK = data_uri(logo("devfusionlab-mark.svg").replace("currentColor", "#2a1416"))
PANJERA_MARK = data_uri(logo("panjera-mark-dark.svg"))
# The Jeeraph logo is mark + wordmark; a 170x170 viewBox keeps only the mark.
EA_MARK = data_uri(logo("educate-afghanistan-mark-dark.svg"))  # the kite, cream body for dark buttons
PANJERA_MARK_LIGHT = data_uri(logo("panjera-mark-light.svg"))
JEERAPH_MARK = data_uri(re.sub(r'viewBox="0 0 594.47 170"', 'viewBox="0 0 170 170"',
                               logo("jeeraph-logo.svg"), count=1))


def svg(width, height, body, title, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">'
            f'<title>{escape(title)}</title>'
            f'<style>{style} {REDUCED_MOTION}</style>{body}</svg>')


def text(x, y, s, size, fill, family=SANS, weight=400, anchor="start", spacing=0, opacity=1):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{spacing}" opacity="{opacity}">{escape(s)}</text>')


def lines(x, y, rows, size, fill, leading, family=SANS):
    return "".join(text(x, y + i * leading, r, size, fill, family) for i, r in enumerate(rows))


# --------------------------------------------------------------------------- header

def rough_line(x1, x2, y, rng, colour, passes=2):
    """A hand-drawn underline in the Rough Notation manner: two wobbly pencil strokes."""
    out = []
    for n in range(passes):
        pts = [(x1 + (x2 - x1) * i / 5 + rng.uniform(-2.5, 2.5), y + rng.uniform(-1.8, 1.8) + n * 3)
               for i in range(6)]
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        out.append(f'<path class="rough r{n}" d="{d}" fill="none" stroke="{colour}" stroke-width="2.6" '
                   f'stroke-linecap="round" stroke-opacity="{0.95 - n * 0.4}"/>')
    return "".join(out)


def header():
    import random
    rng = random.Random(5)
    w, h = 1200, 340
    cx, cy, r = 1010, 150, 92  # the avatar
    small = [(742, 74), (766, 230), (860, 48), (880, 300), (1140, 60), (1160, 290),
             (800, 150), (1150, 170), (920, 40), (1100, 310), (730, 300), (860, 110)]
    edges = [(0, 2), (2, 8), (8, 4), (4, 7), (7, 5), (5, 9), (9, 3), (3, 1), (1, 10), (10, 6),
             (6, 0), (6, 11), (11, 2)]
    parts = [
        f'<defs><pattern id="grid" width="16" height="16" patternUnits="userSpaceOnUse">'
        f'<rect x="0" y="0" width="3" height="3" fill="{AMBER}" opacity="0.12"/></pattern>'
        f'<radialGradient id="glow" cx="{cx / w:.3f}" cy="{cy / h:.3f}" r="0.4">'
        f'<stop offset="0" stop-color="{AMBER}" stop-opacity="0.35"/>'
        f'<stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="frame"><path d="{notched(0, 0, w, h)}"/></clipPath>'
        f'<clipPath id="disc"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
        f'<clipPath id="typed"><rect class="type" x="60" y="190" width="0" height="44"/></clipPath></defs>',
        f'<g clip-path="url(#frame)"><rect width="{w}" height="{h}" fill="{INK}"/>'
        f'<rect width="{w}" height="{h}" fill="url(#grid)"/>'
        f'<rect width="{w}" height="{h}" fill="url(#glow)"/>',
    ]
    palette = [AMBER, PALE, ORANGE, "#c09048", "#a06850"]
    for i in range(18):
        x, size = rng.randrange(690, 1190), rng.choice((4, 6, 8))
        parts.append(f'<rect class="fall p{i}" x="{x}" y="-20" width="{size}" height="{size}" '
                     f'fill="{rng.choice(palette)}" opacity="{rng.uniform(0.25, 0.6):.2f}"/>')
    parts.append('</g>')
    parts.append(f'<path d="{notched(1, 1, w - 2, h - 2)}" fill="none" stroke="{LINE}" stroke-width="2"/>')

    # a faint network behind the character
    for a, b in edges:
        (x1, y1), (x2, y2) = small[a], small[b]
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{AMBER}" '
                     f'stroke-opacity="0.16" stroke-width="1"/>')
    for i, (x, y) in enumerate(small):
        parts.append(f'<rect class="tw t{i % 4}" x="{x - 3}" y="{y - 3}" width="6" height="6" fill="{PALE}" opacity="0.5"/>')

    # the character from the profile picture, in a ring that pulses in pixel steps
    parts += [
        f'<circle class="halo" cx="{cx}" cy="{cy}" r="{r + 10}" fill="none" stroke="{AMBER}" stroke-width="2" stroke-opacity="0.5"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{r + 4}" fill="none" stroke="{SHADOW}" stroke-width="4"/>',
        f'<g class="bob"><image href="{AVATAR}" x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" '
        f'clip-path="url(#disc)" style="image-rendering: pixelated; image-rendering: crisp-edges"/></g>',
    ]

    # how to say the name, under the avatar: a pixel speaker, sound waves, syllables lit in turn
    sx, sy = cx - 104, 296
    parts.append(pixels(sx, sy - 6, ["..#...", ".##...", "###...", "###...", ".##...", "..#..."], CREAM, 4))
    for i, rr in enumerate((11, 18, 25)):
        parts.append(f'<path class="wave v{i}" d="M{sx + 8} {sy - 6 - rr * 0.7} A{rr} {rr} 0 0 1 {sx + 8} {sy - 6 + rr * 0.7}" '
                     f'fill="none" stroke="{AMBER}" stroke-width="2" stroke-linecap="round"/>')
    syl = [("ho", MUTED), ("ma", MUTED), ("YOON", AMBER)]
    x = sx + 46
    for i, (part, colour) in enumerate(syl):
        parts.append(f'<text class="syl s{i}" x="{x}" y="{sy}" font-family="{MONO}" font-size="20" font-weight="700" '
                     f'fill="{colour}" letter-spacing="1">{part}</text>')
        x += len(part) * 12.6 + 5
        if i < 2:
            parts.append(text(x, sy, "·", 15, FAINT, MONO))
            x += 17
    parts.append(text(sx + 46, sy + 20, "rhymes with moon", 12.5, FAINT, MONO, spacing=0.5))

    # the tagline is typed out; three runs with fixed widths so the underline lands under "building things"
    lead, mid, tail = "I like solving problems and ", "building things", ", and I'm always learning."
    lead_w, mid_w, tail_w, gap = 278, 160, 262, 8  # the gap stands in for the space SVG drops
    x0 = 64
    parts += [
        text(64, 104, "SOFTWARE ENGINEER · TECH LEAD · FOUNDER", 14, AMBER, MONO, 500, spacing=3),
        text(65, 173, "Homayoon Behroozian", 52, AMBER, MONO, 700, spacing=-1),  # pixel drop shadow
        text(62, 170, "Homayoon Behroozian", 52, CREAM, MONO, 700, spacing=-1),
        f'<g clip-path="url(#typed)">'
        f'<text x="{x0}" y="218" font-family="{SANS}" font-size="21" fill="{MUTED}" textLength="{lead_w}" '
        f'lengthAdjust="spacing">{escape(lead)}</text>'
        f'<text x="{x0 + lead_w + gap}" y="218" font-family="{SANS}" font-size="21" fill="{CREAM}" textLength="{mid_w}" '
        f'lengthAdjust="spacing">{escape(mid)}</text>'
        f'<text x="{x0 + lead_w + gap + mid_w}" y="218" font-family="{SANS}" font-size="21" fill="{MUTED}" textLength="{tail_w}" '
        f'lengthAdjust="spacing">{escape(tail)}</text></g>',
        rough_line(x0 + lead_w + gap - 2, x0 + lead_w + gap + mid_w + 2, 226, rng, AMBER),
        f'<rect class="cursor" x="{x0}" y="201" width="10" height="21" fill="{AMBER}"/>',
        text(64, 282, "Falls Church, Virginia  ·  Java  ·  TypeScript  ·  Python  ·  Google Cloud",
             14, FAINT, MONO, spacing=0.5),
    ]
    total = lead_w + gap + mid_w + tail_w
    style = (
        ".tw { animation: tw 6s steps(3) infinite; }"
        ".t1 { animation-delay: 1.5s; } .t2 { animation-delay: 3s; } .t3 { animation-delay: 4.5s; }"
        "@keyframes tw { 0%, 100% { opacity: 0.25; } 50% { opacity: 0.8; } }"
        ".fall { animation: fall 12s linear infinite; }"
        + "".join(f".p{i} {{ animation-duration: {9 + (i * 7) % 11:.1f}s; animation-delay: -{(i * 3.7) % 12:.1f}s; }}"
                  for i in range(18))
        + "@keyframes fall { from { transform: translateY(0); } to { transform: translateY(380px); } }"
        ".halo { transform-box: fill-box; transform-origin: center; animation: halo 3.2s steps(8) infinite; }"
        ".wave { opacity: 0; animation: wave 2.4s steps(1) infinite; }"
        ".v1 { animation-delay: 0.3s; } .v2 { animation-delay: 0.6s; }"
        "@keyframes wave { 0% { opacity: 0; } 20% { opacity: 1; } 70% { opacity: 1; } 71% { opacity: 0; } }"
        ".syl { animation: say 2.4s steps(1) infinite; }"
        f".s0 {{ animation-name: say0; }} .s1 {{ animation-name: say1; }} .s2 {{ animation-name: say2; }}"
        f"@keyframes say0 {{ 20% {{ fill: {CREAM}; }} 36% {{ fill: {MUTED}; }} }}"
        f"@keyframes say1 {{ 36% {{ fill: {CREAM}; }} 52% {{ fill: {MUTED}; }} }}"
        f"@keyframes say2 {{ 52% {{ fill: {PALE}; }} 80% {{ fill: {AMBER}; }} }}"
        "@keyframes halo { 0% { transform: scale(0.96); opacity: 0.9; } 100% { transform: scale(1.18); opacity: 0; } }"
        ".bob { animation: bob 2.4s steps(2) infinite; }"
        "@keyframes bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }"
        f".type {{ animation: type 2.2s steps(70) 0.6s forwards; }}"
        f"@keyframes type {{ to {{ width: {total + 8}px; }} }}"
        f".cursor {{ animation: cur 2.2s steps(70) 0.6s forwards, blink 1.1s steps(1) 2.8s infinite; }}"
        f"@keyframes cur {{ to {{ transform: translateX({total + 6}px); }} }}"
        "@keyframes blink { 50% { opacity: 0; } }"
        ".rough { stroke-dasharray: 640; stroke-dashoffset: 640; animation: draw 0.8s ease-out forwards; }"
        ".r0 { animation-delay: 2.9s; } .r1 { animation-delay: 3.3s; }"
        "@keyframes draw { to { stroke-dashoffset: 0; } }"
        f"@media (prefers-reduced-motion: reduce) {{ .type {{ width: {total + 8}px; }} .rough {{ stroke-dasharray: none; }} "
        f".cursor {{ transform: translateX({total + 6}px); }} .fall {{ opacity: 0.2; }} }}"
    )
    title = ("Homayoon Behroozian. Software engineer, tech lead and founder. I like solving problems and "
             "building things, and I'm always learning.")
    return svg(w, h, "".join(parts), title, style)


# --------------------------------------------------------------------------- cards

def notched(x, y, w, h, n=PX * 2):
    """Path of a rectangle whose corners are cut off square, n units wide."""
    return (f"M{x + n} {y} H{x + w - n} V{y + n} H{x + w} V{y + h - n} H{x + w - n} V{y + h} "
            f"H{x + n} V{y + h - n} H{x} V{y + n} H{x + n} Z")


def card_frame(w, h, bg, border):
    return (f'<path d="{notched(1, 1, w - 2, h - 2)}" fill="{bg}" stroke="{border}" stroke-width="2"/>')


def pill(x_right, y, label, colour, live=False):
    width = len(label) * 7.6 + (42 if live else 28)
    x = x_right - width
    dot = (f'<rect class="live" x="{x + 13}" y="{y + 10}" width="8" height="8" fill="{colour}"/>' if live else "")
    tx = x + (30 if live else 14)
    return (f'<path d="{notched(x, y, width, 28, PX)}" fill="none" '
            f'stroke="{colour}" stroke-opacity="0.7" stroke-width="2"/>{dot}'
            + text(tx, y + 18.5, label, 12, colour, MONO, 500, spacing=1.6))


def devfusionlab_card():
    w, h = 1200, 230
    body = [
        card_frame(w, h, PANEL, LINE),
        f'<image href="{DFL_MARK}" x="56" y="70" width="128" height="82"/>',
        text(232, 74, "THE STUDIO", 12, AMBER, MONO, 500, spacing=3),
        text(232, 122, "Dev Fusion Lab", 40, CREAM, MONO, 700, spacing=-0.5),
        text(232, 160, "Software, automation, media and training for businesses in Northern Virginia.",
             19, MUTED),
        text(232, 188, "It's also where I build Panjera and Jeeraph.", 19, MUTED),
        f'<path d="{notched(958, 54, 186, 40, PX)}" fill="none" stroke="{AMBER}" stroke-opacity="0.7" stroke-width="2"/>',
        text(1051, 79, "devfusionlab.com  ↗", 14, CREAM, MONO, anchor="middle"),
    ]
    return svg(w, h, "".join(body), "Dev Fusion Lab: software, automation, media and training for "
               "businesses in Northern Virginia. It's also where I build Panjera and Jeeraph.")


def product_card(*, bg, border, mark, mark_w, mark_h, status, live, accent, name, tagline,
                 body_rows, stack, url, title, ink, muted, faint):
    w, h = 600, 380
    parts = [
        card_frame(w, h, bg, border),
        f'<image href="{mark}" x="40" y="38" width="{mark_w}" height="{mark_h}"/>',
        pill(560, 44, status, accent, live),
        text(40, 150, name, 36, ink, MONO, 700, spacing=-0.5),
        text(40, 186, tagline, 19, accent),
        lines(40, 226, body_rows, 17, muted, 25),
        f'<line x1="40" y1="324" x2="560" y2="324" stroke="{border}"/>',
        text(40, 354, stack, 12.5, faint, MONO, 500, spacing=1),
        text(560, 354, f"{url}  ↗", 14, accent, MONO, 500, "end"),
    ]
    style = (".live { animation: live 2.4s ease-in-out infinite; }"
             "@keyframes live { 0%, 100% { opacity: 1; } 50% { opacity: 0.25; } }")
    return svg(w, h, "".join(parts), title, style)


def panjera_card():
    return product_card(
        bg="#1e1b15", border="rgba(246,237,222,0.14)", mark=PANJERA_MARK, mark_w=46, mark_h=67,
        status="LIVE", live=True, accent="#eead37", ink="#f6edde", muted="#b9af9c", faint="#7d7566",
        name="Panjera",
        tagline="An education platform you deploy as your own.",
        body_rows=["Interactive books in several languages, with a tutor",
                   "that cites its sources. An MCP server gives AI",
                   "assistants 104 tools to work inside the product.",
                   "Running on Google Cloud for Educate Afghanistan."],
        stack="JAVA · SPRING BOOT · REACT · PYTHON · NEO4J", url="panjera.com",
        title="Panjera, live: an education platform you deploy as your own. Interactive books in "
              "several languages, with a tutor that cites its sources. An MCP server gives AI "
              "assistants 104 tools to work inside the product. Running on Google Cloud for "
              "Educate Afghanistan.")


def jeeraph_card():
    return product_card(
        bg="#151c13", border="rgba(249,238,220,0.14)", mark=JEERAPH_MARK, mark_w=64, mark_h=64,
        status="VERSION 1", live=False, accent="#e38027", ink="#f9eedc", muted="#b9af9c", faint="#7d7566",
        name="Jeeraph",
        tagline="The workbench for winning work and delivering it.",
        body_rows=["Find and qualify work, then write the proposal.",
                   "When you win, run the projects, requests and",
                   "contracts in the same place, with your company's",
                   "knowledge kept in one library."],
        stack="JAVA 21 · SPRING BOOT · REACT 19 · POSTGRESQL", url="jeeraph.com",
        title="Jeeraph, version 1: the workbench for winning work and delivering it. Find and "
              "qualify work, then write the proposal. When you win, run the projects, requests and "
              "contracts in the same place, with your company's knowledge kept in one library.")


# --------------------------------------------------------------------------- stack

STACK = [
    ("Languages", ["Java 21", "TypeScript", "Python", "JavaScript", "SQL"]),
    ("Backend", ["Spring Boot 3", "FastAPI", "Node.js", "REST APIs", "OpenAPI", "OAuth 2.1",
                 "Microservices", "SSE streaming", "State machines"]),
    ("Frontend", ["React 19", "Vite", "Electron"]),
    ("Data", ["PostgreSQL", "MongoDB", "Neo4j", "MySQL", "OpenSearch", "Data migrations", "OCR ingestion"]),
    ("Cloud", ["Google Cloud Run", "Firebase Auth", "Secret Manager", "AWS S3", "Lambda", "CloudFormation",
               "ECS", "Docker", "GitHub Actions", "Jenkins", "Maven"]),
    ("AI", ["Anthropic", "OpenAI", "Gemini", "LiteLLM", "MCP servers", "Agent runtimes", "Tool calling",
            "Structured outputs", "Grounded retrieval", "Embeddings", "Knowledge graphs", "Guardrails",
            "Realtime voice", "Claude Code", "Codex"]),
    ("Quality", ["Playwright", "Selenium", "Cucumber", "REST Assured", "Postman", "WireMock", "pytest", "Vitest",
                 "JUnit 5", "TestNG", "Testcontainers", "ArchUnit", "JMeter", "Gatling", "axe-core", "Section 508 · WCAG"]),
    ("Also", ["UX research", "Graphic design", "Curriculum design", "Technical discovery", "Agile coaching"]),
]


def stack_panel():
    w, chip_h, gap, top, left, right = 1200, 42, 10, 40, 210, 48
    rows, y = [], top
    for label, chips in STACK:  # wrap chips into lines so no row runs off the panel
        line, x, y0 = [], left, y
        for chip in chips:
            cw = len(chip) * 9.4 + 34
            if x + cw > w - right:
                x, y = left, y + chip_h + gap
            line.append((x, y, cw, chip))
            x += cw + gap
        rows.append((label, y0, line))
        y += chip_h + 24
    h = y + top - 24
    parts = [card_frame(w, h, PANEL, LINE)]
    for label, y0, line in rows:
        parts.append(text(48, y0 + 27, label.upper(), 13, AMBER, MONO, 500, spacing=2.4))
        for x, y, cw, chip in line:
            parts.append(f'<path d="{notched(x, y, cw, chip_h, PX)}" '
                         f'fill="rgba(255,160,0,0.06)" stroke="{LINE}"/>')
            parts.append(text(x + cw / 2, y + 27.5, chip, 17, CREAM, anchor="middle"))
    title = "Tools I use. " + " ".join(f"{label}: {', '.join(chips)}." for label, chips in STACK)
    return svg(w, h, "".join(parts), title)


# --------------------------------------------------------------------------- timeline

SHOW_EMPLOYERS = True  # False swaps organisation names for a plain description

TIMELINE = [  # years, title, organisation (named / unnamed), note, still running?
    ("2024 · now", "Technical Lead · Java Developer", ("Internal Revenue Service", "a federal agency"),
     "Technical lead on a data platform that holds hundreds of millions of records; "
     "designed its Version 4 data model and API contract.", True),
    ("2023 · 2024", "SDET", ("Internal Revenue Service", "the same agency"),
     "Designed the team's automated test solution across API, contract, data and end-to-end layers.", False),
    ("2022 · 2024", "Co-founder · CEO", ("TEK School", "a technology school"),
     "Ran the school with a team of sixteen and taught about 1,000 people software engineering "
     "and test automation.", False),
    ("2021 · 2022", "Software Engineer in Test", ("FINRA", "a financial regulator"),
     "Test frameworks for the APIs behind regulated stock market data.", False),
    ("2020 · now", "Founder", ("Dev Fusion Lab", "Dev Fusion Lab"),
     "My own studio. Panjera is in production; Jeeraph is in build.", True),
    ("2020 · 2021", "SDET", ("Internal Revenue Service", "a federal agency"),
     "Reusable Java frameworks for functional, regression and accessibility testing of tax applications.", False),
    ("2019 · 2020", "Automation Engineer · QA Lead", ("USPTO", "a federal agency"),
     "Sole quality owner for an internal audit system; took it from manual testing to automated regression.", False),
    ("2015 · 2018", "SDET", ("Atos", "a consultancy"),
     "Java, Selenium, REST Assured and JMeter frameworks for client delivery teams.", False),
]


def timeline():
    w, row_h, top, spine_x = 1200, 82, 44, 196
    h = top + row_h * len(TIMELINE) + 8
    parts = [card_frame(w, h, PANEL, LINE),
             f'<line class="spine" x1="{spine_x}" y1="{top}" x2="{spine_x}" y2="{h - 36}" '
             f'stroke="{AMBER}" stroke-opacity="0.3" stroke-width="2" stroke-dasharray="4 4"/>']
    for i, (years, title, (named, plain), note, current) in enumerate(TIMELINE):
        y = top + i * row_h + 14
        org = named if SHOW_EMPLOYERS else plain
        colour = AMBER if current else CREAM
        parts.append(f'<g class="row r{i}">')
        parts.append(text(48, y + 6, years, 13, FAINT, MONO, 500, spacing=1))
        parts.append(f'<rect x="{spine_x - 6}" y="{y - 6}" width="12" height="12" fill="{PANEL}" stroke="{colour}" stroke-width="2"/>')
        if current:
            parts.append(f'<rect class="live" x="{spine_x - 2}" y="{y - 2}" width="4" height="4" fill="{colour}"/>')
        parts.append(text(228, y + 7, title, 20, CREAM, SANS, 600))
        parts.append(text(228 + len(title) * 10.4 + 18, y + 7, org, 15, FAINT, MONO))
        parts.append(text(228, y + 36, note, 15, MUTED))
        parts.append('</g>')
    style = (
        ".spine { stroke-dasharray: 2000; stroke-dashoffset: 2000; animation: draw 2.2s ease-out forwards; }"
        "@keyframes draw { to { stroke-dashoffset: 0; } }"
        ".row { opacity: 0; animation: rise 0.7s ease-out forwards; }"
        + "".join(f".r{i} {{ animation-delay: {0.15 + i * 0.18:.2f}s; }}" for i in range(len(TIMELINE)))
        + "@keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }"
        ".live { animation: live 2.4s ease-in-out infinite; }"
        "@keyframes live { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }"
        "@media (prefers-reduced-motion: reduce) { .row { opacity: 1; } .spine { stroke-dasharray: none; } }"
    )
    title = "Where I've worked. " + " ".join(
        f"{years}: {t}, {n if SHOW_EMPLOYERS else p}. {note}" for years, t, (n, p), note, _ in TIMELINE)
    return svg(w, h, "".join(parts), title, style)


# --------------------------------------------------------------------------- credentials

CERTS = [  # title, issuer, year
    ("Oracle Certified Professional, Java SE 11 Developer", "Oracle", "2025"),
    ("MySQL 8.0 Database Developer, Oracle Certified Professional", "Oracle", "2025"),
    ("AWS Certified Cloud Practitioner", "Amazon Web Services", "2025"),
    ("Google UX Design Professional Certificate", "Google", "2025"),
    ("Oracle Certified Associate, Java SE 8 Programmer", "Oracle", "2020"),
    ("ISTQB Certified Tester, Foundation Level", "ISTQB", "2018"),
]
DEGREES = [  # title, school, note
    ("MS, Learning Experience Design and Educational Technology", "Western Governors University", ""),
    ("BS, Management Information Systems, minor in Computer Science", "North Dakota State University", ""),
    ("MicroMasters, Statistics and Data Science", "MIT on edX", "in progress"),
]


def pixels(x, y, rows, colour, unit=3):
    """Draw a sprite from rows of '#' and '.', centred on (x, y)."""
    h, w = len(rows), len(rows[0])
    out = []
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == "#":
                out.append(f'<rect x="{x + (c - w / 2) * unit:.1f}" y="{y + (r - h / 2) * unit:.1f}" '
                           f'width="{unit}" height="{unit}" fill="{colour}"/>')
    return "".join(out)


def rosette(x, y):
    """A medal: a ring with a ribbon."""
    return pixels(x, y, ["..###..", ".#...#.", "#..#..#", "#.###.#", "#..#..#", ".#...#.", "..###..",
                         ".##.##.", ".#...#."], AMBER)


def mortarboard(x, y):
    return pixels(x, y, ["....#....", "..#####..", "#########", "..#####.#", "...###..#", "........#"], AMBER)


def credentials():
    w, row_h, top, col2 = 1200, 60, 44, 620
    rows = max(len(CERTS), len(DEGREES))
    h = top + 34 + row_h * rows + 10
    parts = [card_frame(w, h, PANEL, LINE),
             text(48, top, "CERTIFICATIONS", 13, GREEN, MONO, 500, spacing=2.4),
             text(col2, top, "EDUCATION", 13, GREEN, MONO, 500, spacing=2.4),
             f'<line x1="{col2 - 40}" y1="{top - 14}" x2="{col2 - 40}" y2="{h - 36}" stroke="{LINE}"/>']
    n = 0
    for i, (title, issuer, year) in enumerate(CERTS):
        y = top + 34 + i * row_h + 18
        parts.append(f'<g class="row r{n}">{rosette(60, y)}' + text(86, y + 5, title, 16, CREAM)
                     + text(86, y + 26, f"{issuer} · {year}", 12.5, FAINT, MONO) + '</g>')
        n += 1
    for i, (title, school, note) in enumerate(DEGREES):
        y = top + 34 + i * row_h + 18
        sub = school + (f" · {note}" if note else "")
        parts.append(f'<g class="row r{n}">{mortarboard(col2 + 12, y)}' + text(col2 + 38, y + 5, title, 16, CREAM)
                     + text(col2 + 38, y + 26, sub, 12.5, FAINT, MONO) + '</g>')
        n += 1
    style = (".row { opacity: 0; animation: rise 0.7s ease-out forwards; }"
             + "".join(f".r{i} {{ animation-delay: {0.1 + i * 0.12:.2f}s; }}" for i in range(n))
             + "@keyframes rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }"
             "@media (prefers-reduced-motion: reduce) { .row { opacity: 1; } }")
    title = ("Certifications: " + "; ".join(f"{t}, {i}, {y}" for t, i, y in CERTS)
             + ". Education: " + "; ".join(f"{t}, {sc}" + (f", {no}" if no else "") for t, sc, no in DEGREES) + ".")
    return svg(w, h, "".join(parts), title, style)


# --------------------------------------------------------------------------- link buttons

def button(label, icon, width):
    h = 52
    parts = [f'<path d="{notched(PX, PX, width - PX - 1, h - PX - 1, PX)}" fill="{SHADOW}"/>',
             f'<path d="{notched(1, 1, width - PX - 1, h - PX - 1, PX)}" fill="{PANEL}" stroke="{AMBER}" '
             f'stroke-width="2"/>', icon,
             text(56, 30, label, 16, CREAM, MONO, 500)]
    return svg(width, h, "".join(parts), label)


def buttons():
    linkedin_icon = (f'<rect x="18" y="11" width="26" height="26" fill="{AMBER}"/>'
                     + text(31, 30, "in", 16, BUTTON_INK, SANS, 700, "middle"))
    # a pen nib, cream with an amber breather hole
    blog_icon = (f'<g transform="rotate(-35 31 26)">'
                 f'<path d="M31 9 L42 21 L36.5 40 L25.5 40 L20 21 Z" fill="none" stroke="{CREAM}" stroke-width="2" stroke-linejoin="round"/>'
                 f'<line x1="31" y1="40" x2="31" y2="28" stroke="{CREAM}" stroke-width="2"/>'
                 f'<circle cx="31" cy="25" r="3" fill="{AMBER}"/></g>')
    # instagram: a camera outline with the lens and the flash
    instagram_icon = (f'<rect x="18" y="13" width="26" height="26" rx="7" fill="none" stroke="{CREAM}" stroke-width="2"/>'
                      f'<circle cx="31" cy="26" r="6" fill="none" stroke="{CREAM}" stroke-width="2"/>'
                      f'<circle cx="38.5" cy="18.5" r="1.8" fill="{AMBER}"/>')
    return {
        "link-linkedin.svg": button("LinkedIn", linkedin_icon, 150),
        "link-devfusionlab.svg": button(
            "Dev Fusion Lab", f'<image href="{DFL_MARK}" x="16" y="15" width="30" height="19"/>', 206),
        "link-panjera.svg": button(
            "Panjera", f'<image href="{PANJERA_MARK}" x="22" y="10" width="19" height="28"/>', 140),
        "link-jeeraph.svg": button(
            "Jeeraph", f'<image href="{JEERAPH_MARK}" x="17" y="10" width="28" height="28"/>', 140),
        "link-blog.svg": button("Blog", blog_icon, 112),
        "link-instagram.svg": button("Instagram", instagram_icon, 162),
        "link-educateafghanistan.svg": button(
            "Educate Afghanistan", f'<image href="{EA_MARK}" x="23" y="7" width="19" height="34"/>', 254),
    }


def main():
    ASSETS.mkdir(exist_ok=True)
    files = {
        "header.svg": header(),
        "card-devfusionlab.svg": devfusionlab_card(),
        "card-panjera.svg": panjera_card(),
        "card-jeeraph.svg": jeeraph_card(),
        "stack.svg": stack_panel(),
        "timeline.svg": timeline(),
        "credentials.svg": credentials(),
        **buttons(),
    }
    for name, content in files.items():
        (ASSETS / name).write_text(content, encoding="utf-8")
        print(f"assets/{name}  {len(content):,} bytes")


if __name__ == "__main__":
    main()
