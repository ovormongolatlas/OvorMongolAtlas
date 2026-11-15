"""Build the Bogd Khanate / MPR areas into src/data/outer-mongolia.json.

Run trace_korostovets.py, period_outlines.py and combine_territories.py first.
Inputs: ../../src/data/period-outlines.json (Outer Mongolia as Korostovets draws
it, closed up to his border with Russia), korostovets-1914-north.json (Russia
and Uriankhai on his map), and ../../src/data/territories.json (the 1930s areas).

No present-day border is used. The outline is Korostovets's (about 1914; the
same line is on his English map of about 1926). From 1933 it is fitted to
Manchukuo as Narangoa and Cribb draw it for the 1930s: where the two overlap,
Manchukuo is kept, and strips left between them are given to the MPR. The
Mongol territories of 1936-1945 are already fitted to Korostovets's line in
combine_territories.py, so they meet it without a gap.
"""
import json
import numpy as np, cv2
from pyproj import Proj
from scipy.ndimage import distance_transform_edt
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

P = Proj(proj='lcc', lat_1=37, lat_2=47, lat_0=43, lon_0=113, ellps='WGS84')
def proj(ring): return Polygon([P(a, b) for a, b in ring]).buffer(0)
def single(g):
    g = g.buffer(0)
    if isinstance(g, MultiPolygon): g = max(g.geoms, key=lambda p: p.area)
    return Polygon(g.exterior)

base = single(proj(json.load(open('../../src/data/period-outlines.json'))['outer']))
russia = proj(json.load(open('korostovets-1914-north.json'))['north'])

T = json.load(open('../../src/data/territories.json'))
manchu = proj(T['manchukuo'])
mmg, claimed, scag, nsag, mj = (proj(T[k]) for k in ('mmg1936', 'mlaagClaimed', 'scag', 'nsag', 'mengjiang1939'))

# raster helpers (1 km cells)
RES = 1000.0
minx, miny, maxx, maxy = base.buffer(200000).bounds
W, H = int((maxx - minx) / RES) + 1, int((maxy - miny) / RES) + 1
def raster(g):
    m = np.zeros((H, W), np.uint8)
    for p in (g.geoms if hasattr(g, 'geoms') else [g]):
        if p.is_empty: continue
        cv2.fillPoly(m, [((np.array(p.exterior.coords) - [minx, miny]) / RES).round().astype(np.int32)], 1)
    return m.astype(bool)
def vector(mask):
    cs, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ps = [Polygon(c[:, 0, :] * RES + [minx, miny]).buffer(0) for c in cs if len(c) >= 3]
    return unary_union(ps).buffer(RES * 1.5) if ps else Polygon()
def close(mask, r):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * int(r / RES) + 1,) * 2)
    return cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_CLOSE, k).astype(bool)
R = raster(russia)
def fit_to(neighbours, wmax=80000):
    """Base outline, giving overlaps to the neighbours and the strips between to the MPR."""
    nb = unary_union(neighbours)
    A = raster(base); N = raster(nb)
    dA = distance_transform_edt(~A) * RES; dN = distance_transform_edt(~N) * RES
    allm = A | N | R
    gap = close(allm, wmax / 2) & ~allm & (dA + dN <= wmax)
    g = unary_union([base, vector(gap)]).difference(nb).difference(russia)
    return single(g.buffer(-200).buffer(200))

variants = {
    'base': base,
    'mpr1933': fit_to([manchu]),
    'mpr1936': fit_to([manchu, mmg]),
    'mpr1937': fit_to([manchu, claimed, scag, nsag]),
    'mpr1940': fit_to([manchu, mj]),
}
# Korostovets marks a small area near Buir Nuur as disputed between Barga and
# Khalkha («Спорная местность между Баргой и Халхой»); it is left white on his
# map, so it is the hole between Outer Mongolia and Manchukuo here.
holes = [Polygon(h) for h in unary_union([variants['mpr1933'], manchu]).buffer(0).interiors]
holes = [h for h in holes if h.area > 500e6]
assert len(holes) == 1, [round(h.area / 1e6) for h in holes]
variants['disputed'] = holes[0].buffer(600).difference(variants['mpr1933']).difference(manchu).buffer(-100).buffer(100)
# From 1933 the 1930s atlas (Narangoa and Cribb) is the source for this frontier, and on it the
# patch lies in the MPR (everything there that is not Manchukuo); so it is given to the MPR from 1933.
for k in ('mpr1933', 'mpr1936', 'mpr1937', 'mpr1940'):
    variants[k] = single(unary_union([variants[k], variants['disputed'].buffer(800)]).difference(manchu).buffer(-200).buffer(200))
variants['mpr1946'] = single(unary_union([base, variants['disputed'].buffer(800)]).buffer(-200).buffer(200))

out = {}
for k, g in variants.items():
    g = g.simplify(1500)
    lon, lat = P(*np.array(g.exterior.coords).T, inverse=True)
    out[k] = [[round(float(a), 3), round(float(b), 3)] for a, b in zip(lon, lat)]
    print(k, len(out[k]), round(g.area / 1e6), 'km2')
json.dump(out, open('../../src/data/outer-mongolia.json', 'w'), separators=(',', ':'))
