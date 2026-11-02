"""Big Five in a Bronkhorst-style language: thick palette-knife bands, shaped canvases,
tiny figures, white shadow-box frames. Writes designs/svg-wb/*.svg; render with render.js wb."""
import math, random, pathlib
from build import elephant, lion, leopard, buffalo, rhino, strip_fill

OUT = pathlib.Path(__file__).resolve().parent.parent / "svg-wb"
OUT.mkdir(exist_ok=True)
W, H = 1200, 1500


def defs(seed):
    return f"""
<filter id="knife" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">
  <feTurbulence type="fractalNoise" baseFrequency="0.0025 0.035" numOctaves="3" seed="{seed}" result="t"/>
  <feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="h"/>
  <feDiffuseLighting in="h" surfaceScale="2.4" lighting-color="#fff" result="l"><feDistantLight azimuth="250" elevation="64"/></feDiffuseLighting>
  <feComposite in="SourceGraphic" in2="l" operator="arithmetic" k1="0.78" k2="0.3" result="lit"/>
  <feComposite in="lit" in2="SourceGraphic" operator="in"/>
</filter>
<filter id="dab" x="-20%" y="-20%" width="140%" height="140%" color-interpolation-filters="sRGB">
  <feGaussianBlur in="SourceAlpha" stdDeviation="5" result="b"/>
  <feTurbulence type="fractalNoise" baseFrequency="0.03 0.08" numOctaves="2" seed="{seed+1}" result="t"/>
  <feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0.5 0 0 0 0" result="tn"/>
  <feComposite in="b" in2="tn" operator="arithmetic" k2="1" k3="0.6" result="h"/>
  <feDiffuseLighting in="h" surfaceScale="7" lighting-color="#fff" result="l"><feDistantLight azimuth="235" elevation="48"/></feDiffuseLighting>
  <feComposite in="SourceGraphic" in2="l" operator="arithmetic" k1="0.8" k2="0.28" result="lit"/>
  <feComposite in="lit" in2="SourceGraphic" operator="in" result="d"/>
  <feGaussianBlur in="SourceAlpha" stdDeviation="3"/><feOffset dx="3" dy="5"/>
  <feComponentTransfer><feFuncA type="linear" slope="0.3"/></feComponentTransfer>
  <feMerge><feMergeNode/><feMergeNode in="d"/></feMerge>
</filter>
<filter id="soft"><feGaussianBlur stdDeviation="0.9"/></filter>
<filter id="lipblur"><feGaussianBlur stdDeviation="2.2"/></filter>
<filter id="drop" x="-10%" y="-10%" width="120%" height="125%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="10"/><feOffset dy="12"/>
  <feComponentTransfer><feFuncA type="linear" slope="0.22"/></feComponentTransfer>
  <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="inner" x="0" y="0" width="1" height="1">
  <feFlood flood-color="#000" flood-opacity="0.35"/><feComposite in2="SourceAlpha" operator="out"/>
  <feGaussianBlur stdDeviation="9"/><feOffset dx="0" dy="6"/>
  <feComposite in2="SourceAlpha" operator="in"/>
</filter>
"""


def tiny(body, x, y, rot, scale, sun=(-1, -0.7), op=0.45):
    """Small figure with a short, soft contact shadow (miniature-figurine look)."""
    L = math.hypot(*sun); ux, uy = sun[0] / L, sun[1] / L
    k = 0.5
    a, b, d = 1 + k*ux*ux, k*ux*uy, 1 + k*uy*uy
    sh = (f'<g transform="translate({x+ux*6:.1f},{y+uy*6:.1f}) matrix({a:.3f},{b:.3f},{b:.3f},{d:.3f},0,0) '
          f'rotate({rot}) scale({scale})" opacity="{op}" filter="url(#soft)"><g fill="#2a2030">{strip_fill(body)}</g></g>')
    return sh + f'<g transform="translate({x},{y}) rotate({rot}) scale({scale})">{body}</g>'


def wavy(x0, x1, y, amp, rnd, n=14):
    pts = [(x0 + (x1 - x0) * i / n, y + rnd.uniform(-amp, amp)) for i in range(n + 1)]
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        d += f" Q{ax:.1f},{ay:.1f} {(ax+bx)/2:.1f},{(ay+by)/2:.1f}"
    return d + f" L{pts[-1][0]:.1f},{pts[-1][1]:.1f}", pts


def lip(edge_d, color):
    """Ridge of thick paint where a knife stroke ends: soft shadow + bright crest."""
    return (f'<path d="{edge_d}" fill="none" stroke="#000" stroke-opacity="0.16" stroke-width="8" '
            f'filter="url(#lipblur)" transform="translate(0,-4)"/>'
            f'<path d="{edge_d}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="{edge_d}" fill="none" stroke="#fff" stroke-opacity="0.4" stroke-width="1.2" '
            f'transform="translate(0,-1.5)"/>')


def lighten(hexc, t):
    r, g, b = (int(hexc[i:i+2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(int(c + (255 - c) * t) for c in (r, g, b))


def h_bands(x, y, w, h, colors, seed, amp=7):
    """Horizontal knife bands, top to bottom, each overlapping the next."""
    rnd = random.Random(seed)
    out = []
    bh = h / len(colors)
    for i, c in enumerate(colors):
        top = y + i * bh + (rnd.uniform(-6, 6) if i else -20)
        edge, _ = wavy(x - 30, x + w + 30, top, amp if i else 0, rnd)
        out.append(f'<path d="{edge} L{x+w+30},{y+h+30} L{x-30},{y+h+30}Z" fill="{c}"/>')
        if i:
            out.append(lip(edge, lighten(c, 0.25)))
    return '<g filter="url(#knife)">' + "".join(out) + "</g>"


def arc_bands(cx, cy, r0, r1, colors, seed):
    """Concentric arcs (largest first) for oval and semicircle canvases."""
    rnd = random.Random(seed)
    out = []
    n = len(colors)
    for i, c in enumerate(colors):
        r = r0 - (r0 - r1) * i / n
        pts = []
        for k in range(73):
            a = math.pi * k / 72
            rr = r + rnd.uniform(-5, 5)
            pts.append((cx - rr * math.cos(a), cy - rr * math.sin(a)))
        d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}" + "".join(f" L{px:.1f},{py:.1f}" for px, py in pts[1:])
        out.append(f'<path d="{d} L{cx+r},{cy+2000} L{cx-r},{cy+2000}Z" fill="{c}"/>')
        if i:
            out.append(lip(d, lighten(c, 0.25)))
    return '<g filter="url(#knife)">' + "".join(out) + "</g>"


def svg(shapes, paint, seed, bg="#ffffff"):
    """shapes: list of (canvas path d, frame path d or None)."""
    clips = "".join(f'<clipPath id="c{i}"><path d="{s}"/></clipPath>' for i, (s, _) in enumerate(shapes))
    frames = ""
    for i, (s, f) in enumerate(shapes):
        if f:
            frames += (f'<g filter="url(#drop)"><path d="{f}" fill="#fbfbfa" stroke="#e6e4df" stroke-width="2"/></g>'
                       f'<path d="{s}" fill="#ecebe7"/>')
        else:
            frames += f'<g filter="url(#drop)"><path d="{s}" fill="#fff"/></g>'
    body = "".join(f'<g clip-path="url(#c{i})">{p}</g>' for i, p in enumerate(paint))
    inner = "".join(f'<path d="{s}" fill="#fff" filter="url(#inner)" opacity="0.6"/>' for s, f in shapes if f)
    edges = "".join(f'<path d="{s}" fill="none" stroke="#000" stroke-opacity="0.12" stroke-width="1.5"/>' for s, _ in shapes)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<defs>{defs(seed)}{clips}</defs><rect width="{W}" height="{H}" fill="{bg}"/>'
            f'{frames}{body}{edges}</svg>')


def rect(x, y, w, h):
    return f"M{x},{y} h{w} v{h} h{-w}Z"


def oval(x, y, w, h):
    r = w / 2
    return f"M{x},{y+r} A{r},{r} 0 0 1 {x+w},{y+r} V{y+h-r} A{r},{r} 0 0 1 {x},{y+h-r}Z"


def semi(cx, base, r):
    return f"M{cx-r},{base} A{r},{r} 0 0 1 {cx+r},{base}Z"


def write(name, s):
    (OUT / f"{name}.svg").write_text(s)


# 1. SEEING RED - Tsavo elephant. Vertical oval, sunset arcs (Abendrot language).
def p1():
    x, y, w, h = 360, 170, 480, 1160
    cols = ["#f9e3a6", "#f7cf7a", "#f4b452", "#f0953a", "#e8712d", "#dc4f25", "#c3321f", "#9a2219", "#6a1712"]
    paint = arc_bands(600, 1500, 1330, 260, cols, 1) + tiny(elephant("#6b2418", "#93402a"), 600, 560, -8, 0.42)
    write("01-seeing-red-tsavo-elephant", svg([(oval(x, y, w, h), None)], [paint], 11))


# 2. PRIDE OF PLACE - Serengeti lion. Semicircle sun, gold bands.
def p2():
    cx, base, r = 600, 1000, 480
    cols = ["#fff3c4", "#fde69a", "#fbd66e", "#f8c34a", "#f4ab32", "#ee9124", "#e2761b"]
    paint = h_bands(cx - r, base - r, 2 * r, r, cols, 2, amp=5) + tiny(lion(), 650, 880, 80, 0.4)
    write("02-pride-of-place-serengeti-lion", svg([(semi(cx, base, r), None)], [paint], 22))


# 3. SPOT ON - Samburu leopard. Square shadow box, acacia canopy as thick green dabs.
def p3():
    rnd = random.Random(3)
    x, y, s = 250, 400, 700
    fx = 40
    paint = h_bands(x, y, s, s, ["#f3c98a", "#efbb76", "#eaad64", "#e4a055"], 30, amp=5)
    greens = ["#2f8a4a", "#3fa05a", "#56b56a", "#7cc77d", "#a6d99a", "#2f8a4a", "#3fa05a"]
    dabs = []
    for row in range(8):
        for col in range(7):
            if rnd.random() < 0.18:
                continue
            cx = x + 20 + col * 110 + rnd.uniform(-30, 30) + (row % 2) * 50
            cy = y + 30 + row * 92 + rnd.uniform(-22, 22)
            rx, ry = rnd.uniform(55, 85), rnd.uniform(38, 58)
            pts = []
            for k in range(10):
                a = 2 * math.pi * k / 10
                f = rnd.uniform(0.8, 1.15)
                pts.append((cx + rx * f * math.cos(a), cy + ry * f * math.sin(a)))
            d = f"M{(pts[0][0]+pts[1][0])/2:.0f},{(pts[0][1]+pts[1][1])/2:.0f}"
            for i in range(1, 11):
                p, q = pts[i % 10], pts[(i + 1) % 10]
                d += f" Q{p[0]:.0f},{p[1]:.0f} {(p[0]+q[0])/2:.0f},{(p[1]+q[1])/2:.0f}"
            dabs.append(f'<path d="{d}Z" fill="{rnd.choice(greens)}"/>')
    paint += '<g filter="url(#dab)">' + "".join(dabs) + "</g>"
    paint += tiny(leopard(), 600, 750, -75, 0.42, op=0.55)
    write("03-spot-on-samburu-leopard",
          svg([(rect(x, y, s, s), rect(x - fx, y - fx, s + 2*fx, s + 2*fx))], [paint], 33))


# 4. HERD MENTALITY - Ngorongoro buffalo. Long horizontal panel, pink cream bands.
def p4():
    rnd = random.Random(4)
    x, y, w, h = 120, 560, 960, 360
    fx = 32
    paint = h_bands(x, y, w, h, ["#fdeef2", "#fbdfe8", "#f8cada", "#f4b3c9", "#ef9bb7", "#e9809f"], 40, amp=5)
    for i in range(9):
        t = i / 8
        paint += tiny(buffalo(), 330 + t * 420 + rnd.uniform(-6, 6), 760 - t * 70 + rnd.uniform(-8, 8),
                      70 + rnd.uniform(-10, 10), 0.26, op=0.5)
    write("04-herd-mentality-ngorongoro-buffalo",
          svg([(rect(x, y, w, h), rect(x - fx, y - fx, w + 2*fx, h + 2*fx))], [paint], 44))


# 5. PLUS ONE - Amboseli black rhino + calf. Diptych, curved sweeps (High Horses language).
def p5():
    rnd = random.Random(5)
    s, gap, y = 470, 40, 520
    xs = [600 - gap/2 - s, 600 + gap/2]
    fx = 30
    paints = []
    for j, x0 in enumerate(xs):
        g = f'<rect x="{x0}" y="{y}" width="{s}" height="{s}" fill="#f2ebdf"/><g filter="url(#knife)">'
        for k in range(5):
            cy = y - 220 + k * 210 + rnd.uniform(-10, 10)
            d = f"M{x0-80},{cy+260} C{x0+120},{cy+120} {x0+300},{cy+40} {x0+s+80},{cy-60}"
            g += f'<path d="{d} L{x0+s+80},{y+s+400} L{x0-80},{y+s+400}Z" fill="{["#f4eee3","#efe6d7","#e9dfcd","#f1e9dc"][k%4]}"/>'
            g += lip(d, "#faf6ef")
        g += "</g>"
        if j == 0:
            g += tiny(rhino(), x0 + 250, y + 270, 35, 0.36, op=0.5)
        else:
            g += tiny(rhino(), x0 + 200, y + 250, 40, 0.22, op=0.5)
        paints.append(g)
    shapes = [(rect(x0, y, s, s), rect(x0 - fx, y - fx, s + 2*fx, s + 2*fx)) for x0 in xs]
    write("05-plus-one-amboseli-rhino", svg(shapes, paints, 55))


if __name__ == "__main__":
    for f in (p1, p2, p3, p4, p5):
        f()
    print(sorted(p.name for p in OUT.iterdir()))
