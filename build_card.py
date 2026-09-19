#!/usr/bin/env python3
"""
Builds dark_mode.svg and light_mode.svg (the neofetch-style profile card).

  1. Edit the PROFILE section below with your own info.
  2. (optional) python make_ascii.py my_photo.jpg      -> new ascii_art.txt
  3. python build_card.py                              -> regenerates both SVGs

The live numbers (Uptime, repos, stars, commits, followers, lines of code) are
placeholders here; today.py refreshes them every day through GitHub Actions.
"""
from xml.sax.saxutils import escape
import today                       # re-use the exact same alignment logic as the daily job

# ═══════════════════════════ PROFILE (edit me) ═══════════════════════════
TITLE = "rounak@das"

# Row types:
#   ("kv", "Key", "value")        -> ". Key: ........ value"     (use "A.B" for a dotted key like Languages.Programming)
#   ("blank",)                    -> empty spacer line
#   ("section", "Contact")        -> "- Contact -————————"
#   ("uptime",)                   -> live "Uptime" line (updated daily)
#   ("stats",)                    -> the 3 live GitHub stat lines (updated daily)
ROWS = [
    ("title",),
    ("uptime",),
    ("kv", "Host", "Parul University"),
    ("kv", "Kernel", "B.Tech CSE (AI & Machine Learning)"),
    ("kv", "IDE", "Visual Studio Code"),
    ("blank",),
    ("kv", "Languages.Programming", "Python, C, C++, Java, JavaScript"),
    ("kv", "Languages.Computer", "HTML, CSS, SQL"),
    # ("kv", "Languages.Real", "English, ..."),          # <- add your spoken languages if you like
    ("blank",),
    ("kv", "Focus", "AI/ML Fundamentals, Python for AI/ML"),
    ("kv", "Core", "OOP, DSA (Basics), DBMS, Problem Solving"),
    ("kv", "Certs.Cloud", "Oracle OCI 2025 AI Foundations Associate"),
    ("kv", "Certs.Other", "Google Analytics, Product Owner"),
    ("kv", "Projects", "Portfolio Site, QR Code Generator"),
    ("blank",),
    ("section", "Contact"),
    ("kv", "Email", "iamrounak2020@gmail.com"),
    ("kv", "LinkedIn", "rounak-d-380827359"),
    ("kv", "GitHub", "Rounak-Das-2007"),
    ("kv", "Location", "Vadodara, Gujarat, India"),
    ("blank",),
    ("section", "GitHub Stats"),
    ("stats",),
]
# ═════════════════════════════════════════════════════════════════════════

ART_FILE = "ascii_art.txt"
W = today.LINE_WIDTH                 # width of the info column (characters)
X_ART, X_INFO, LINE_H = 15, 390, 20

THEMES = {
    "dark_mode.svg": dict(bg="#161b22", text="#c9d1d9", key="#ffa657", value="#a5d6ff",
                          add="#3fb950", dele="#f85149", cc="#616e7f"),
    "light_mode.svg": dict(bg="#f6f8fa", text="#24292f", key="#953800", value="#0a3069",
                           add="#1a7f37", dele="#cf222e", cc="#c2cfde"),
}


def rule(label):
    """'- Contact -——————————-—-'  (exactly W characters)"""
    fill = W - len(label) - len(" -") - len("-—-")
    return f'<tspan x="{X_INFO}" y="{{y}}">{escape(label)}</tspan> -' + "—" * fill + "-—-"


def kv_line(key, value):
    key_html = ".".join(f'<tspan class="key">{escape(part)}</tspan>' for part in key.split("."))
    seg = W - (2 + len(key) + 1) - len(value)
    if seg < 3:
        raise SystemExit(f'Line too long ({-seg + 3} chars over): "{key}: {value}" - shorten it.')
    dots = " " + "." * (seg - 2) + " "
    return (f'<tspan x="{X_INFO}" y="{{y}}" class="cc">. </tspan>{key_html}:'
            f'<tspan class="cc">{dots}</tspan><tspan class="value">{escape(value)}</tspan>')


def blank_line():
    return f'<tspan x="{X_INFO}" y="{{y}}" class="cc">. </tspan>'


def uptime_line():
    return (f'<tspan x="{X_INFO}" y="{{y}}" class="cc">. </tspan><tspan class="key">Uptime</tspan>:'
            '<tspan class="cc" id="age_data_dots"> ..... </tspan><tspan class="value" id="age_data">0</tspan>')


STATS = [
    f'<tspan x="{X_INFO}" y="{{y}}" class="cc">. </tspan><tspan class="key">Repos</tspan>:'
    '<tspan class="cc" id="repo_data_dots"> .... </tspan><tspan class="value" id="repo_data">0</tspan> '
    '{<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">0</tspan>} | '
    '<tspan class="key">Stars</tspan>:<tspan class="cc" id="star_data_dots"> ... </tspan>'
    '<tspan class="value" id="star_data">0</tspan>',

    f'<tspan x="{X_INFO}" y="{{y}}" class="cc">. </tspan><tspan class="key">Commits</tspan>:'
    '<tspan class="cc" id="commit_data_dots"> ... </tspan><tspan class="value" id="commit_data">0</tspan> | '
    '<tspan class="key">Followers</tspan>:<tspan class="cc" id="follower_data_dots"> ... </tspan>'
    '<tspan class="value" id="follower_data">0</tspan>',

    f'<tspan x="{X_INFO}" y="{{y}}" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:'
    '<tspan class="cc" id="loc_data_dots">. </tspan><tspan class="value" id="loc_data">0</tspan> ( '
    '<tspan class="addColor" id="loc_add">0</tspan><tspan class="addColor">++</tspan>, '
    '<tspan id="loc_del_dots"> </tspan><tspan class="delColor" id="loc_del">0</tspan>'
    '<tspan class="delColor">--</tspan> )',
]


def info_lines():
    out = []
    for row in ROWS:
        kind = row[0]
        if kind == "title":
            out.append(rule(TITLE))
        elif kind == "section":
            out.append(rule("- " + row[1]))
        elif kind == "kv":
            out.append(kv_line(row[1], row[2]))
        elif kind == "blank":
            out.append(blank_line())
        elif kind == "uptime":
            out.append(uptime_line())
        elif kind == "stats":
            out.extend(STATS)
        else:
            raise SystemExit(f"Unknown row type: {kind}")
    return out


def build():
    art = [l.rstrip("\n") for l in open(ART_FILE, encoding="utf-8")]
    info = info_lines()
    n = max(len(art), len(info))
    art += [""] * (n - len(art))
    height = 30 + LINE_H * n
    width = 985

    for filename, c in THEMES.items():
        svg = [
            "<?xml version='1.0' encoding='UTF-8'?>",
            f'<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" '
            f'width="{width}px" height="{height}px" font-size="16px">',
            "<style>",
            "@font-face {",
            "src: local('Consolas'), local('Consolas Bold');",
            "font-family: 'ConsolasFallback';",
            "font-display: swap;",
            "-webkit-size-adjust: 109%;",
            "size-adjust: 109%;",
            "}",
            f".key {{fill: {c['key']};}}",
            f".value {{fill: {c['value']};}}",
            f".addColor {{fill: {c['add']};}}",
            f".delColor {{fill: {c['dele']};}}",
            f".cc {{fill: {c['cc']};}}",
            "text, tspan {white-space: pre;}",
            "</style>",
            f'<rect width="{width}px" height="{height}px" fill="{c["bg"]}" rx="15"/>',
            f'<text x="{X_ART}" y="30" fill="{c["text"]}" class="ascii">',
        ]
        for i, line in enumerate(art):
            svg.append(f'<tspan x="{X_ART}" y="{30 + LINE_H * i}">{escape(line)}</tspan>')
        svg.append("</text>")
        svg.append(f'<text x="{X_INFO}" y="30" fill="{c["text"]}">')
        for i, line in enumerate(info):
            svg.append(line.replace("{y}", str(30 + LINE_H * i)))
        svg.append("</text>")
        svg.append("</svg>")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(svg) + "\n")

        # fill in placeholder numbers + dots so the card looks right before the first Action run
        today.svg_overwrite(filename, today.daily_readme(today.UPTIME_SINCE), 0, 0, 0, 0, 0, [0, 0, 0])
        print(f"wrote {filename}  ({width}x{height}, {len(info)} info rows, {len(art)} art rows)")


if __name__ == "__main__":
    build()
