"""Kenya series, minimal: flat two-tone field (sky + ground), one small animal on the horizon.
Writes designs/svg-plain/*.svg; render with `node render.js plain`."""
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "svg-plain"
OUT.mkdir(exist_ok=True)
W, H = 1200, 1500


# ---- side-view animals: feet at y=0, facing right ----
def giraffe(c="#b9783a", patch="#6e3d1c", dark="#4a2a14"):
    patches = "".join(f'<path d="{d}" fill="{patch}"/>' for d in [
        "M-24,-104 l10,-4 l6,8 l-8,7 l-9,-3Z", "M-6,-108 l12,-3 l4,9 l-10,6 l-7,-5Z",
        "M14,-104 l11,-2 l3,9 l-9,5 l-7,-6Z", "M-14,-90 l10,-2 l3,8 l-9,3Z", "M6,-90 l10,-1 l2,8 l-9,2Z",
        "M34,-118 l7,-2 l3,8 l-7,3Z", "M44,-138 l6,-2 l3,8 l-6,3Z", "M53,-158 l6,-2 l2,8 l-6,2Z",
        "M62,-178 l5,-2 l2,7 l-5,2Z"])
    return f"""
<path d="M-38,-104 Q-48,-86 -46,-66" stroke="{c}" stroke-width="2.2" fill="none"/>
<path d="M-48,-70 l3,10 l3,-10Z" fill="{dark}"/>
<path d="M-30,-96 L-34,-48 L-30,0 M-20,-94 L-18,-48 L-22,0" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>
<path d="M32,-100 L34,-50 L30,0 M42,-102 L46,-50 L44,0" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>
<path d="M-42,-100 C-40,-118 0,-124 30,-120 C44,-118 50,-108 46,-96 C40,-86 -10,-84 -36,-90Z" fill="{c}"/>
<path d="M28,-112 L42,-122 L76,-196 L64,-200 Z" fill="{c}"/>
<path d="M31,-116 C41,-150 55,-180 63,-199" stroke="{dark}" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.8"/>
<path d="M62,-202 C68,-210 82,-206 92,-196 C94,-192 90,-189 86,-190 C78,-191 70,-192 64,-194Z" fill="{c}"/>
<path d="M68,-205 l-1,-10 M73,-206 l1,-10" stroke="{dark}" stroke-width="2.5" stroke-linecap="round"/>
<circle cx="76" cy="-199" r="1.4" fill="{dark}"/>
{patches}
<path d="M-34,-6 l0,6 M-22,-6 l0,6 M30,-6 l0,6 M44,-6 l0,6" stroke="{dark}" stroke-width="6"/>
"""


def elephant(c="#6d5f5a", dark="#4b3f3b", tusk="#f4ecdc"):
    return f"""
<path d="M-52,-78 Q-62,-60 -58,-40" stroke="{dark}" stroke-width="2.5" fill="none"/>
<rect x="-46" y="-50" width="20" height="50" rx="6" fill="{dark}"/>
<rect x="18" y="-50" width="20" height="50" rx="6" fill="{dark}"/>
<path d="M-56,-60 C-60,-100 -20,-112 18,-108 C44,-106 56,-92 56,-70 C56,-50 46,-38 30,-36 L-40,-36 C-52,-38 -56,-48 -56,-60Z" fill="{c}"/>
<rect x="-30" y="-48" width="20" height="48" rx="6" fill="{c}"/>
<rect x="30" y="-48" width="20" height="48" rx="6" fill="{c}"/>
<path d="M40,-96 C56,-112 80,-104 82,-84 C84,-74 80,-66 78,-60 C84,-40 84,-18 88,-4 L78,-2 C72,-18 70,-40 66,-54 C54,-56 44,-66 40,-80Z" fill="{c}"/>
<path d="M44,-98 C30,-96 26,-76 30,-60 C34,-50 46,-50 52,-58 C56,-70 54,-88 44,-98Z" fill="{dark}" opacity="0.55"/>
<path d="M70,-62 Q84,-54 94,-60" stroke="{tusk}" stroke-width="4" fill="none" stroke-linecap="round"/>
<circle cx="70" cy="-84" r="1.8" fill="#2a2220"/>
"""


def rhino(c="#7b7570", dark="#57524e", horn="#d9cfbf"):
    return f"""
<path d="M-52,-50 Q-58,-36 -54,-26" stroke="{dark}" stroke-width="2" fill="none"/>
<rect x="-42" y="-28" width="15" height="28" rx="4" fill="{dark}"/>
<rect x="22" y="-28" width="15" height="28" rx="4" fill="{dark}"/>
<path d="M-54,-38 C-56,-62 -30,-72 0,-70 C20,-72 36,-74 46,-62 C54,-52 52,-34 40,-26 L-44,-24 C-52,-26 -54,-32 -54,-38Z" fill="{c}"/>
<rect x="-30" y="-28" width="15" height="28" rx="4" fill="{c}"/>
<rect x="32" y="-28" width="15" height="28" rx="4" fill="{c}"/>
<path d="M40,-58 C54,-62 70,-52 84,-36 C88,-30 86,-22 78,-20 C66,-18 52,-24 42,-30Z" fill="{c}"/>
<path d="M48,-60 l-4,-12 l9,8Z M56,-60 l0,-11 l6,9Z" fill="{dark}"/>
<path d="M76,-34 C80,-46 86,-56 92,-62 C90,-50 88,-40 84,-30Z" fill="{horn}"/>
<path d="M66,-42 C68,-48 70,-52 73,-55 C73,-49 72,-44 70,-40Z" fill="{horn}"/>
<path d="M10,-68 C2,-54 0,-40 4,-28" stroke="{dark}" stroke-width="1.5" fill="none" opacity="0.6"/>
<circle cx="64" cy="-46" r="1.5" fill="#2a2622"/>
"""


def lion(c="#c48a3f", mane="#6a3415", dark="#8a5a26"):
    return f"""
<path d="M-50,-16 C-66,-12 -76,-6 -88,-4" stroke="{c}" stroke-width="3" fill="none" stroke-linecap="round"/>
<ellipse cx="-90" cy="-4" rx="4" ry="3.5" fill="{mane}"/>
<path d="M-56,-14 C-58,-34 -40,-42 -20,-40 L30,-38 C44,-36 50,-26 48,-12 L46,0 L-50,0 C-56,-2 -56,-8 -56,-14Z" fill="{c}"/>
<ellipse cx="-38" cy="-16" rx="20" ry="16" fill="{dark}" opacity="0.35"/>
<path d="M30,-6 L74,-6 C80,-6 80,0 74,0 L30,0Z" fill="{c}"/>
<path d="M26,-30 C24,-56 44,-70 60,-64 C76,-58 78,-38 70,-24 C62,-14 40,-12 30,-18Z" fill="{mane}"/>
<path d="M50,-50 C56,-58 70,-56 74,-48 L80,-36 C80,-30 74,-28 68,-28 C58,-28 50,-34 50,-50Z" fill="{c}"/>
<path d="M54,-54 l2,-6 l5,4Z" fill="{mane}"/>
<circle cx="68" cy="-44" r="1.5" fill="#2a1a0e"/>
<ellipse cx="79" cy="-34" rx="2" ry="1.5" fill="#3a2010"/>
"""


def piece(name, title, sky_top, sky_bot, ground_top, ground_bot, horizon, animal, ax, scale,
          mode="shadow", shadow_k=1.4, flip=False, place=""):
    cx, cy, cw, ch = 150, 150, 900, 1140  # canvas
    hy = cy + ch * horizon
    feet = hy + 18 * scale
    fl = "scale(-1,1)" if flip else ""
    fig = f'<g transform="translate({ax},{feet:.1f}) scale({scale}) {fl}">{animal}</g>'
    if mode == "shadow":
        cast = (f'<g transform="translate({ax},{feet:.1f}) matrix(1,0,{shadow_k},-0.32,0,0) scale({scale}) {fl}" '
                f'opacity="0.28" filter="url(#blur)"><g fill="#1a1020">{animal_flat(animal)}</g></g>')
    else:  # reflection in water
        cast = (f'<g transform="translate({ax},{feet:.1f}) scale({scale},{-scale*0.9}) {fl}" opacity="0.32" '
                f'filter="url(#wave)">{animal}</g>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky_top}"/><stop offset="1" stop-color="{sky_bot}"/></linearGradient>
<linearGradient id="gnd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ground_top}"/><stop offset="1" stop-color="{ground_bot}"/></linearGradient>
<filter id="blur"><feGaussianBlur stdDeviation="1.6"/></filter>
<filter id="wave"><feTurbulence type="fractalNoise" baseFrequency="0.01 0.3" numOctaves="1" seed="4"/>
  <feDisplacementMap in="SourceGraphic" scale="6"/><feGaussianBlur stdDeviation="0.8"/></filter>
<filter id="drop" x="-10%" y="-10%" width="120%" height="125%"><feGaussianBlur in="SourceAlpha" stdDeviation="12"/>
  <feOffset dy="14"/><feComponentTransfer><feFuncA type="linear" slope="0.25"/></feComponentTransfer>
  <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="cv"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}"/></clipPath>
</defs>
<rect width="{W}" height="{H}" fill="#f3f1ed"/>
<g filter="url(#drop)"><rect x="{cx-22}" y="{cy-22}" width="{cw+44}" height="{ch+44}" fill="#c9a77c"/></g>
<rect x="{cx-14}" y="{cy-14}" width="{cw+28}" height="{ch+28}" fill="#2b2622"/>
<g clip-path="url(#cv)">
  <rect x="{cx}" y="{cy}" width="{cw}" height="{hy-cy+1:.0f}" fill="url(#sky)"/>
  <rect x="{cx}" y="{hy:.0f}" width="{cw}" height="{cy+ch-hy:.0f}" fill="url(#gnd)"/>
  {cast}{fig}
</g>
<text x="600" y="{cy+ch+90}" text-anchor="middle" font-family="Caladea, 'DejaVu Serif', serif" font-size="40" fill="#2b2622">{title}</text>
<text x="600" y="{cy+ch+128}" text-anchor="middle" font-family="Inter, sans-serif" font-size="17" letter-spacing="3" fill="#8a8178">{place}</text>
</svg>"""


def animal_flat(s):
    import re
    s = re.sub(r'fill="(?!none)[^"]*"', 'fill="#1a1020"', s)
    return re.sub(r'stroke="[^"]*"', 'stroke="#1a1020"', s)


PIECES = [
    ("01-higher-management-giraffe", "Higher Management", "#fde3c8", "#f7b98a", "#ee7a32", "#d9551f",
     0.56, giraffe(), 560, 1.05, "shadow", 1.6, False, "GIRAFFE · MAASAI MARA"),
    ("02-trunk-call-elephant", "Trunk Call", "#fbe3e4", "#f4c3c8", "#d4507f", "#b23466",
     0.6, elephant(), 640, 1.15, "shadow", -1.5, False, "ELEPHANT · AMBOSELI"),
    ("03-lunch-break-lion", "Lunch Break", "#fff3c2", "#fbe08a", "#2f9a63", "#1d7a4c",
     0.52, lion(), 560, 1.25, "shadow", 1.7, False, "LION · SAMBURU"),
    ("04-do-not-disturb-rhino", "Do Not Disturb", "#e3f6f6", "#bfe8ea", "#2f64c4", "#1d4596",
     0.58, rhino(), 600, 1.25, "reflect", 0, True, "RHINO · LEWA"),
]

if __name__ == "__main__":
    for p in PIECES:
        (OUT / f"{p[0]}.svg").write_text(piece(*p))
    print(sorted(x.name for x in OUT.iterdir()))
