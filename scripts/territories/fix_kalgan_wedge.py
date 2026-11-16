"""Close the sliver of Manchukuo that pokes between the Mongolian Allied League and
South Chahar areas north-east of Kalgan.

Manchukuo (Narangoa and Cribb, 1935-1940) reaches south-west to about 115.28 E, 41.05 N,
into ground that lies west of the Chahar-Jehol boundary (about 116 E in the China
Postal Atlas sheet) and is enclosed on two sides by the Mongol territory (Nakamura's
Chahar League line) and the South Chahar outline (the Japanese map of Mengjiang). It is
a tracing mismatch between three maps, not a territorial claim. The sliver is the part
of Manchukuo south of 41.395 N and west of 115.80 E that neither neighbour covers; it is
split between the two neighbours by nearest edge, the convention the atlas uses for thin
strips between its territories.

Edits src/data/territories.json: mlaagRuled, scag and mengjiang1939.
Run from the repository root:  python3 scripts/territories/fix_kalgan_wedge.py
"""
import json
from shapely.geometry import Polygon, box
from shapely.ops import unary_union

PATH = 'src/data/territories.json'
T = json.load(open(PATH))


def geom(key):
    r = T[key]
    rings = [r] if isinstance(r[0][0], (int, float)) else r
    return unary_union([Polygon(x).buffer(0) for x in rings])


def store(key, g, like):
    single = isinstance(T[like][0][0], (int, float))
    polys = [g] if g.geom_type == 'Polygon' else list(g.geoms)
    rings = [[list(map(lambda c: round(c, 5), p)) for p in poly.exterior.coords] for poly in polys]
    T[key] = rings[0] if (single and len(rings) == 1) else rings


M, G, S = geom('manchukuo'), geom('mlaagRuled'), geom('scag')
cut = box(115.2, 40.9, 115.80, 41.395)
sliver = M.intersection(cut).difference(G.union(S))
sliver = unary_union([p for p in (sliver.geoms if hasattr(sliver, 'geoms') else [sliver]) if p.area > 1e-6])
print('sliver area (deg^2):', round(sliver.area, 5))

# nearest-edge split
near_g = sliver.intersection(G.buffer(0.5).difference(S.buffer(0))).buffer(0)
pts_g, pts_s = [], []
from shapely.ops import voronoi_diagram
# simple split: a point goes to the neighbour whose boundary is closer
grid = sliver.buffer(0)
cells = []
step = 0.004
minx, miny, maxx, maxy = sliver.bounds
x = minx
from shapely.geometry import Point
while x <= maxx:
    y = miny
    while y <= maxy:
        c = box(x, y, x + step, y + step)
        if c.intersects(sliver):
            cp = c.centroid
            (pts_g if G.distance(cp) <= S.distance(cp) else pts_s).append(c)
        y += step
    x += step
to_g = unary_union(pts_g).intersection(sliver) if pts_g else sliver.buffer(0).difference(sliver)
to_s = unary_union(pts_s).intersection(sliver) if pts_s else sliver.buffer(0).difference(sliver)
print('to MLAAG', round(to_g.area, 5), 'to South Chahar', round(to_s.area, 5))

g2 = unary_union([G, to_g.buffer(0.0015)])
s2 = unary_union([S, to_s.buffer(0.0015)])
store('mlaagRuled', g2, 'mlaagRuled')
store('scag', s2, 'scag')
if 'mengjiang1939' in T:
    mj = geom('mengjiang1939')
    store('mengjiang1939', unary_union([mj, sliver.buffer(0.0015)]), 'mengjiang1939')
json.dump(T, open(PATH, 'w'), ensure_ascii=False)
print('ok')
