"""Period outlines from Korostovets's map, into src/data/period-outlines.json.

Run trace_korostovets.py first. Inputs beside this script:
  korostovets-1914-outer.json, korostovets-1914-north.json,
  korostovets-1914-coverage.json        (from trace_korostovets.py)
  ne_50m_land.geojson                   (Natural Earth coastline, physical only)
  ne_10m_admin_0_countries.geojson      (only for Korea, and for Russia where the
                                         period map does not reach; see below)

Writes:
  outer           Outer Mongolia (Khalkha), with the strip between the traced
                  orange fill and the traced Russian/Uriankhai fill closed;
  russiaMongolia, tuvaMongolia, russiaManchuria
                  the period borders with Russia and Uriankhai, as lines;
  qing            the Qing Empire to 1911: all land in the map frame except
                  Russia (as Korostovets draws it) and Korea.
Two pieces are not from Korostovets: Korea's border with the Qing, the Yalu
River (his map stops short of it), and Russia in the far north-east corner of
the frame, beyond his map's edge. Both are noted where they are used.
"""
import json
import numpy as np, cv2
from pyproj import Proj
from scipy.ndimage import distance_transform_edt
from shapely.geometry import Polygon, MultiPolygon, LineString, Point, box, shape
from shapely.ops import unary_union

P = Proj(proj='lcc', lat_1=37, lat_2=47, lat_0=43, lon_0=113, ellps='WGS84')
def proj(ring): return Polygon([P(a, b) for a, b in ring]).buffer(0)
def single(g):
    g = g.buffer(0)
    if isinstance(g, MultiPolygon): g = max(g.geoms, key=lambda p: p.area)
    return Polygon(g.exterior)
def ll_ring(g, tol=1500):
    g = g.simplify(tol)
    lon, lat = P(*np.array(g.exterior.coords).T, inverse=True)
    return [[round(float(a), 3), round(float(b), 3)] for a, b in zip(lon, lat)]
def ll_line(coords, tol=1000):
    l = LineString(coords).simplify(tol)
    lon, lat = P(*np.array(l.coords).T, inverse=True)
    out = [[round(float(a), 3), round(float(b), 3)] for a, b in zip(lon, lat)]
    return out if out[0][0] <= out[-1][0] else out[::-1]

K = proj(json.load(open('korostovets-1914-outer.json'))['outer'])
N = proj(json.load(open('korostovets-1914-north.json'))['north'])
COVER = proj(json.load(open('korostovets-1914-coverage.json'))['coverage'])
CLIP = Polygon([P(x, y) for x, y in [(88, 30), (140, 30), (140, 56), (88, 56)]]).buffer(0)

# Close the printed border band between Outer Mongolia and Russia: strips under 40 km
# lying between the two fills go to Outer Mongolia.
RES = 1000.0
minx, miny, maxx, maxy = K.buffer(150000).bounds
W, Hh = int((maxx - minx) / RES) + 1, int((maxy - miny) / RES) + 1
def raster(g):
    m = np.zeros((Hh, W), np.uint8)
    for p in (g.geoms if hasattr(g, 'geoms') else [g]):
        if p.is_empty: continue
        cv2.fillPoly(m, [((np.array(p.exterior.coords) - [minx, miny]) / RES).round().astype(np.int32)], 1)
    return m.astype(bool)
def vector(mask):
    cs, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ps = [Polygon(c[:, 0, :] * RES + [minx, miny]).buffer(0) for c in cs if len(c) >= 3]
    return unary_union(ps).buffer(RES * 1.5) if ps else Polygon()
A, B = raster(K), raster(N)
dA, dB = distance_transform_edt(~A) * RES, distance_transform_edt(~B) * RES
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))
gap = cv2.morphologyEx((A | B).astype(np.uint8), cv2.MORPH_CLOSE, k).astype(bool) & ~(A | B) & (dA + dB <= 40000)
outer = single(unary_union([K, vector(gap)]).difference(N).buffer(-200).buffer(200))

# Lines: the parts of a boundary that run along a neighbour, away from the map's edge.
inside_map = COVER.buffer(-15000)
def runs(ring, keep):
    pts = list(ring.coords)
    # densify so short gaps do not split runs
    dense = []
    for a, b in zip(pts[:-1], pts[1:]):
        n = max(1, int(Point(a).distance(Point(b)) / 1000))
        dense += [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n)]
    flags = [keep(Point(p)) for p in dense]
    if all(flags): return [dense]
    start = flags.index(False)
    dense, flags = dense[start:] + dense[:start], flags[start:] + flags[:start]
    out, cur = [], []
    for p, f in zip(dense, flags):
        if f: cur.append(p)
        elif cur: out.append(cur); cur = []
    if cur: out.append(cur)
    return [r for r in out if LineString(r).length > 50000]

near_N = N.buffer(4000)
mongolia_runs = runs(outer.exterior, lambda p: near_N.contains(p) and inside_map.contains(p))
SPLIT = P(99.0, 50)[0]   # west of about 99°E Outer Mongolia borders Uriankhai, east of it Russia proper
mongolia_line = max(mongolia_runs, key=lambda r: LineString(r).length)
tuva = [p for p in mongolia_line if p[0] < SPLIT]
russia_mn = [p for p in mongolia_line if p[0] >= SPLIT]

east_of_mongolia = P(116.3, 49.8)[0]
far_from_outer = outer.buffer(8000)
manchu_runs = runs(N.exterior, lambda p: p.x > east_of_mongolia and not far_from_outer.contains(p) and inside_map.contains(p))
# The Amur's northern bend runs off the top of Korostovets's map (north of this map's
# frame), which splits the line in two; the pieces are joined in order.
russia_manchu = [p for r in sorted(manchu_runs, key=lambda r: min(q[0] for q in r))
                 for p in (r if r[0][0] <= r[-1][0] else r[::-1])]

# Qing Empire to 1911.
def ne_country(names):
    gs = []
    for f in json.load(open('ne_10m_admin_0_countries.geojson'))['features']:
        if f['properties']['ADMIN'] in names:
            g = shape(f['geometry'])
            for p in (g.geoms if hasattr(g, 'geoms') else [g]):
                if p.bounds[0] < 140 and p.bounds[2] > 80 and 25 < p.bounds[1] < 60:
                    gs.append(Polygon([P(x, y) for x, y in p.exterior.coords]).buffer(0))
    return unary_union(gs)
land = unary_union([Polygon([P(x, y) for x, y in p.exterior.coords]).buffer(0)
                    for f in json.load(open('ne_50m_land.geojson'))['features']
                    for p in (shape(f['geometry']).geoms if hasattr(shape(f['geometry']), 'geoms') else [shape(f['geometry'])])
                    if p.bounds[0] < 140 and p.bounds[2] > 80])
korea = ne_country({'North Korea', 'South Korea'})
russia_beyond_map = ne_country({'Russia'}).difference(COVER)
# Join the traced Russia to Russia beyond the map's edge, closing the seam where they meet.
russia = unary_union([N, russia_beyond_map]).buffer(15000).buffer(-15000)
qing = single(land.intersection(CLIP).difference(russia).difference(korea).buffer(-500).buffer(500))

out = {
    'outer': ll_ring(outer),
    'qing': ll_ring(qing, 2500),
    'russiaMongolia': ll_line(russia_mn),
    'tuvaMongolia': ll_line(tuva),
    'russiaManchuria': ll_line(russia_manchu),
}
json.dump(out, open('../../src/data/period-outlines.json', 'w'), separators=(',', ':'))
for k, v in out.items(): print(k, len(v), v[0], v[-1])
