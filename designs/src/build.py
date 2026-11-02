"""Generates the Big Five design studies as SVG. Render with render.js."""
import math, random, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "svg"
OUT.mkdir(exist_ok=True)

W, H = 1200, 1500  # wall image size


def defs_filters(seed):
    return f"""
<filter id="crackle" x="0" y="0" width="1" height="1" color-interpolation-filters="sRGB">
  <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="4" seed="{seed}" result="t"/>
  <feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="h"/>
  <feDiffuseLighting in="h" surfaceScale="4" lighting-color="#fff" result="light"><feDistantLight azimuth="225" elevation="58"/></feDiffuseLighting>
  <feComposite in="SourceGraphic" in2="light" operator="arithmetic" k1="0.8" k2="0.32" result="lit"/>
  <feComposite in="lit" in2="SourceGraphic" operator="in"/>
</filter>
<filter id="impasto" x="0" y="0" width="1" height="1" color-interpolation-filters="sRGB">
  <feTurbulence type="fractalNoise" baseFrequency="0.0025 0.045" numOctaves="4" seed="{seed+3}" result="t"/>
  <feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="h"/>
  <feDiffuseLighting in="h" surfaceScale="9" lighting-color="#fff" result="light"><feDistantLight azimuth="235" elevation="50"/></feDiffuseLighting>
  <feComposite in="SourceGraphic" in2="light" operator="arithmetic" k1="0.85" k2="0.3" result="lit"/>
  <feComposite in="lit" in2="SourceGraphic" operator="in"/>
</filter>
<filter id="grain" x="0" y="0" width="1" height="1" color-interpolation-filters="sRGB">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="{seed+7}" result="t"/>
  <feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.18 -0.05" result="g"/>
  <feComposite in="g" in2="SourceGraphic" operator="in" result="g2"/>
  <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="g2"/></feMerge>
</filter>
<filter id="patch" x="0" y="0" width="1" height="1">
  <feTurbulence type="fractalNoise" baseFrequency="0.005" numOctaves="3" seed="{seed+9}"/>
  <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  3.2 0 0 0 -1.1"/>
</filter>
<mask id="patchy" maskUnits="userSpaceOnUse" x="0" y="0" width="1200" height="1500"><rect width="1200" height="1500" fill="#fff" filter="url(#patch)"/></mask>
<filter id="soft"><feGaussianBlur stdDeviation="1.4"/></filter>
<filter id="drop" x="-10%" y="-10%" width="120%" height="125%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="14"/><feOffset dx="0" dy="18"/>
  <feComponentTransfer><feFuncA type="linear" slope="0.28"/></feComponentTransfer>
  <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
"""


def with_shadow(body, x, y, rot, scale, sdx, sdy, skew=None, op=0.4, stretch=2.4):
    """Shadow = silhouette stretched along (sdx,sdy) direction, anchored at the figure."""
    L = math.hypot(sdx, sdy) or 1
    ux, uy = sdx / L, sdy / L
    k = stretch - 1
    a, b, c, d = 1 + k*ux*ux, k*ux*uy, k*ux*uy, 1 + k*uy*uy
    shift = 0.35 * L
    shadow = (f'<g transform="translate({x+ux*shift:.1f},{y+uy*shift:.1f}) matrix({a:.3f},{b:.3f},{c:.3f},{d:.3f},0,0) rotate({rot}) scale({scale})" '
              f'opacity="{op}" filter="url(#soft)"><g fill="#1d1830" stroke="none">{strip_fill(body)}</g></g>')
    fig = f'<g transform="translate({x},{y}) rotate({rot}) scale({scale})">{body}</g>'
    return shadow + fig


def strip_fill(s):
    import re
    s = re.sub(r'fill="[^"]*"', '', s)
    s = re.sub(r'stroke="(?!none)[^"]*"', 'stroke="#1d1830"', s)
    return s


# ---- animals, top-down, head toward -y, roughly unit = 1px at scale 1 ----
def elephant(skin="#a5523a", hi="#c77352"):
    return f"""
<path d="M-6,52 q2,14 -2,22" stroke="{skin}" stroke-width="2.5" fill="none"/>
<ellipse cx="0" cy="10" rx="30" ry="44" fill="{skin}"/>
<ellipse cx="-6" cy="4" rx="16" ry="30" fill="{hi}" opacity="0.5"/>
<path d="M-10,-40 C-40,-58 -70,-40 -62,-8 C-56,14 -36,14 -24,2 C-18,-10 -12,-24 -10,-40Z" fill="{skin}" stroke="#5a2414" stroke-width="1.6"/>
<path d="M10,-40 C40,-58 70,-40 62,-8 C56,14 36,14 24,2 C18,-10 12,-24 10,-40Z" fill="{skin}" stroke="#5a2414" stroke-width="1.6"/>
<ellipse cx="0" cy="-38" rx="17" ry="19" fill="{hi}"/>
<path d="M-7,-52 q-4,-14 -1,-22 M7,-52 q4,-14 1,-22" stroke="#f3ead8" stroke-width="3.5" fill="none" stroke-linecap="round"/>
<path d="M0,-54 C3,-72 -10,-84 -4,-104 C-2,-110 4,-110 4,-104" stroke="{skin}" stroke-width="8" fill="none" stroke-linecap="round"/>
"""


def lion():
    rnd = random.Random(7)
    mane = "".join(
        f'<path d="M{18*math.cos(a):.1f},{-30+18*math.sin(a):.1f} l{9*math.cos(a+rnd.uniform(-.3,.3)):.1f},{9*math.sin(a+rnd.uniform(-.3,.3)):.1f}" '
        f'stroke="{rnd.choice(["#6b3414","#7d4019","#5a2a10","#8f4d1e"])}" stroke-width="5" stroke-linecap="round"/>'
        for a in [i*2*math.pi/46 for i in range(46)])
    return f"""
<path d="M2,62 C16,80 28,74 30,90" stroke="#b7802f" stroke-width="3" fill="none"/>
<circle cx="30" cy="92" r="4" fill="#4a2a12"/>
<path d="M-16,-12 L-14,-62 Q-10,-68 -6,-62 L-6,-14Z" fill="#cf9842"/>
<path d="M16,-12 L14,-62 Q10,-68 6,-62 L6,-14Z" fill="#cf9842"/>
<ellipse cx="0" cy="20" rx="23" ry="46" fill="#d6a04a"/>
<path d="M-18,50 C-30,58 -28,70 -18,66Z M18,50 C30,58 28,70 18,66Z" fill="#c38a3a"/>
<ellipse cx="3" cy="14" rx="10" ry="30" fill="#e8bd6c" opacity="0.6"/>
{mane}
<circle cx="0" cy="-30" r="19" fill="#7a3f17"/>
<path d="M-9,-26 Q0,-18 9,-26 L6,-48 Q0,-54 -6,-48Z" fill="#d9a552"/>
<ellipse cx="0" cy="-50" rx="4" ry="3" fill="#4a2a12"/>
<circle cx="-12" cy="-40" r="4" fill="#9a5520"/><circle cx="12" cy="-40" r="4" fill="#9a5520"/>
"""


def leopard():
    spots = "".join(
        f'<circle cx="{random.uniform(-12,12):.1f}" cy="{random.uniform(-26,40):.1f}" r="{random.uniform(1.6,2.8):.1f}" '
        f'fill="none" stroke="#2b1a0e" stroke-width="1.4"/>' for _ in range(34))
    return f"""
<path d="M0,44 C10,70 -4,92 6,118" stroke="#d9a447" stroke-width="5" fill="none" stroke-linecap="round"/>
<path d="M6,118 l1,8" stroke="#2b1a0e" stroke-width="5" stroke-linecap="round"/>
<ellipse cx="0" cy="8" rx="14" ry="40" fill="#e1ad52"/>
<path d="M-12,-20 l-14,-10 l3,-5 l14,8Z M12,30 l18,10 l-3,5 l-18,-8Z M-12,32 l-20,6 l1,6 l20,-5Z" fill="#d79f45"/>
{spots}
<ellipse cx="0" cy="-38" rx="10" ry="11" fill="#e6b45a"/>
<circle cx="-7" cy="-46" r="3" fill="#c68f3c"/><circle cx="7" cy="-46" r="3" fill="#c68f3c"/>
"""


def buffalo():
    return """
<path d="M0,40 q-3,10 2,16" stroke="#1f1a1a" stroke-width="2" fill="none"/>
<ellipse cx="0" cy="8" rx="20" ry="34" fill="#2a2321"/>
<ellipse cx="-4" cy="2" rx="9" ry="22" fill="#4a3d38" opacity="0.6"/>
<ellipse cx="0" cy="-30" rx="10" ry="12" fill="#2a2321"/>
<path d="M-4,-36 C-22,-44 -28,-30 -20,-22 M4,-36 C22,-44 28,-30 20,-22" stroke="#6b5a48" stroke-width="5" fill="none" stroke-linecap="round"/>
<rect x="-8" y="-40" width="16" height="6" rx="3" fill="#6b5a48"/>
"""


def rhino(body="#4f4945", hi="#6f6863"):
    return f"""
<path d="M0,54 q-2,8 2,12" stroke="{body}" stroke-width="2" fill="none"/>
<path d="M0,-34 C28,-34 30,10 27,32 C24,58 -24,58 -27,32 C-30,10 -28,-34 0,-34Z" fill="{body}"/>
<path d="M-8,-20 C-20,0 -18,30 -6,40" stroke="{hi}" stroke-width="9" fill="none" stroke-linecap="round" opacity="0.7"/>
<path d="M-17,-28 C-19,-48 -15,-70 -11,-84 Q0,-92 11,-84 C15,-70 19,-48 17,-28Z" fill="{body}"/>
<path d="M-14,-34 C-24,-36 -26,-46 -20,-48 C-16,-44 -14,-40 -12,-36Z" fill="{hi}"/>
<path d="M14,-34 C24,-36 26,-46 20,-48 C16,-44 14,-40 12,-36Z" fill="{hi}"/>
<path d="M-5,-84 Q0,-110 5,-84Z" fill="#e6dccb"/>
<path d="M-3.5,-68 Q0,-80 3.5,-68Z" fill="#e6dccb"/>
"""


def person_red():
    return """
<ellipse cx="0" cy="2" rx="7" ry="5" fill="#d1271f"/>
<path d="M-7,2 L-3,14 L3,14 L7,2Z" fill="#b41f18"/>
<circle cx="0" cy="-2" r="3.3" fill="#2a1a12"/>
<line x1="6" y1="-6" x2="10" y2="16" stroke="#3a2a1a" stroke-width="1.2"/>
"""


def acacia(rnd):
    # flat-top canopy from above: clustered green blobs + visible branch
    blobs = []
    for _ in range(260):
        a = rnd.uniform(0, 2 * math.pi); r = 150 * math.sqrt(rnd.random())
        x, y = r * math.cos(a) * 1.15, r * math.sin(a) * 0.9
        c = rnd.choice(["#2f7a3a", "#3c8f45", "#4fa64f", "#2a6a34", "#67b85a"])
        blobs.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(9,20):.1f}" fill="{c}"/>')
    return "".join(blobs)


def cracks(x, y, w, h, size, width, color, op, seed, wobble=0.35):
    rnd = random.Random(seed)
    rh = size * 0.866
    cols = int(w / size) + 3; rows = int(h / rh) + 3
    P = {}
    for j in range(rows):
        for i in range(cols):
            P[i, j] = (x - size + i*size + (j % 2)*size/2 + rnd.uniform(-1, 1)*size*wobble,
                       y - rh + j*rh + rnd.uniform(-1, 1)*rh*wobble)
    tris = []
    for j in range(rows - 1):
        for i in range(cols - 1):
            if j % 2 == 0:
                tris += [((i, j), (i+1, j), (i, j+1)), ((i+1, j), (i+1, j+1), (i, j+1))]
            else:
                tris += [((i, j), (i+1, j), (i+1, j+1)), ((i, j), (i+1, j+1), (i, j+1))]
    cen = [tuple(sum(P[v][k] for v in t)/3 for k in (0, 1)) for t in tris]
    edges = {}
    for ti, t in enumerate(tris):
        for e in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            edges.setdefault(frozenset(e), []).append(ti)
    segs = []
    for e, ts in edges.items():
        if len(ts) != 2 or rnd.random() < 0.06:
            continue
        (x1, y1), (x2, y2) = cen[ts[0]], cen[ts[1]]
        mx = (x1+x2)/2 + rnd.uniform(-1, 1)*size*0.12; my = (y1+y2)/2 + rnd.uniform(-1, 1)*size*0.12
        sw = width * rnd.uniform(0.55, 1.5)
        segs.append(f'<path d="M{x1:.1f},{y1:.1f} Q{mx:.1f},{my:.1f} {x2:.1f},{y2:.1f}" stroke-width="{sw:.2f}"/>')
    return (f'<g fill="none" stroke="{color}" stroke-opacity="{op}" stroke-linecap="round">' + "".join(segs) + '</g>'
            f'<g fill="none" stroke="#fff" stroke-opacity="{op*0.5}" stroke-linecap="round" transform="translate(1.2,1.2)">'
            + "".join(segs[::2]) + '</g>')


def crackle_ground(x, y, w, h, fill, crack, seed, big=58, small=20):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" filter="url(#crackle)"/>'
            + '<g mask="url(#patchy)">' + cracks(x, y, w, h, small, 1.0, crack, 0.6, seed+1) + '</g>'
            + cracks(x, y, w, h, big, 2.2, crack, 0.85, seed))


def canvas_frame(shape_d, paint, title_note=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{{DEFS}}<clipPath id="cv"><path d="{shape_d}"/></clipPath></defs>
<rect width="{W}" height="{H}" fill="#f4f2ee"/>
<g filter="url(#drop)"><path d="{shape_d}" fill="#fff"/></g>
<g clip-path="url(#cv)">{paint}</g>
<path d="{shape_d}" fill="none" stroke="#000" stroke-opacity="0.08" stroke-width="2"/>
</svg>"""


def rect_d(x, y, w, h):
    return f"M{x},{y} h{w} v{h} h{-w}Z"


def oval_d(x, y, w, h):
    r = w / 2
    return (f"M{x},{y+r} A{r},{r} 0 0 1 {x+w},{y+r} V{y+h-r} A{r},{r} 0 0 1 {x},{y+h-r}Z")


def write(name, svg, seed):
    (OUT / f"{name}.svg").write_text(svg.replace("{DEFS}", defs_filters(seed)))


# 1. SEEING RED - Tsavo elephant, oval canvas
def p1():
    rnd = random.Random(1)
    x, y, w, h = 300, 160, 600, 1180
    grad = """<linearGradient id="g1" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f2a65a"/><stop offset="0.55" stop-color="#d4572b"/><stop offset="1" stop-color="#8e2417"/></linearGradient>"""
    paint = f"""{grad}{crackle_ground(x, y, w, h, "url(#g1)", "#5a1a0e", 101)}
    {with_shadow(elephant("#c0603f", "#e08a62"), 640, 900, -12, 1.3, -60, -75, op=0.5)}
    """
    write("01-seeing-red-tsavo-elephant", canvas_frame(oval_d(x, y, w, h), paint), 11)


# 2. PRIDE OF PLACE - Serengeti lion on gold knife-swept grass
def p2():
    x, y, w, h = 200, 230, 800, 1040
    bands = ""
    cols = ["#f7d774", "#f4c94f", "#f0b93a", "#eba62c", "#e39222", "#d97b1c"]
    bh = h / len(cols)
    for i, c in enumerate(cols):
        bands += f'<rect x="{x}" y="{y+i*bh-2:.0f}" width="{w}" height="{bh+4:.0f}" fill="{c}"/>'
    paint = f"""<g filter="url(#impasto)">{bands}</g>
    {with_shadow(lion(), 430, 880, 18, 0.9, 70, -45, op=0.42)}
    """
    write("02-pride-of-place-serengeti-lion", canvas_frame(rect_d(x, y, w, h), paint), 22)


# 3. SPOT ON - Samburu leopard in acacia, from above
def p3():
    rnd = random.Random(3)
    x, y, w, h = 230, 250, 740, 1000
    canopy = acacia(rnd)
    paint = f"""{crackle_ground(x, y, w, h, "#e2763a", "#6e2a10", 303)}
    <g transform="translate(560,820) skewX(-28)" opacity="0.32" filter="url(#soft)"><g fill="#1d1830">{strip_fill(canopy)}</g></g>
    <g transform="translate(640,700)">
      <g filter="url(#grain)">{canopy}</g>
      <path d="M-150,40 C-60,20 20,30 150,-30" stroke="#4a2c1a" stroke-width="10" fill="none" stroke-linecap="round"/>
      <g transform="translate(10,18) rotate(-80) scale(0.95)">{leopard()}</g>
    </g>"""
    write("03-spot-on-samburu-leopard", canvas_frame(rect_d(x, y, w, h), paint), 33)


# 4. HERD MENTALITY - Ngorongoro buffalo crossing pink soda flat
def p4():
    rnd = random.Random(4)
    x, y, w, h = 150, 380, 900, 740
    grad = """<linearGradient id="g4" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#fbd2df"/><stop offset="0.6" stop-color="#f29bb8"/><stop offset="1" stop-color="#e5739a"/></linearGradient>"""
    herd = ""
    for i in range(11):
        t = i / 10
        hx = 260 + t * 640 + rnd.uniform(-14, 14)
        hy = 900 - t * 330 + rnd.uniform(-20, 20)
        herd += with_shadow(buffalo(), hx, hy, 62 + rnd.uniform(-8, 8), 0.6, 40, 26, op=0.38)
    paint = f"""{grad}{crackle_ground(x, y, w, h, "url(#g4)", "#a8385e", 404)}
    <path d="M{x},{y+h} L{x},{y+h-160} C{x+200},{y+h-120} {x+260},{y+h-40} {x+380},{y+h}Z" fill="#c9443d" opacity="0.55" filter="url(#crackle)"/>
    {herd}"""
    write("04-herd-mentality-ngorongoro-buffalo", canvas_frame(rect_d(x, y, w, h), paint), 44)


# 5. BLACK & WHITE - Amboseli black rhino + calf on white salt pan, red-shuka herder far off
def p5():
    x, y, w, h = 250, 200, 700, 1100
    paint = f"""{crackle_ground(x, y, w, h, "#f6f3ec", "#8a8178", 505)}
    {with_shadow(rhino(), 540, 840, 20, 1.15, -70, -55, op=0.42)}
    {with_shadow(rhino(), 650, 905, 28, 0.6, -40, -32, op=0.42)}
    {with_shadow(person_red(), 800, 420, 0, 1.5, -30, -38, op=0.35)}
    """
    write("05-black-and-white-amboseli-rhino", canvas_frame(rect_d(x, y, w, h), paint), 55)


for f in (p1, p2, p3, p4, p5):
    random.seed(f.__name__)
    f()
print("svgs:", sorted(p.name for p in OUT.iterdir()))
