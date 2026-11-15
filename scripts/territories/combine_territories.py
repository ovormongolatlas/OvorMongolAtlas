"""Combine the traced territories into src/data/territories.json.

Run trace_nc_1935_1940.py, trace_jp_mengjiang.py, trace_korostovets.py and
period_outlines.py first. The frontier with Outer Mongolia and Russia is
Korostovets's (about 1914), the only period map of the whole line used here;
no present-day border is used.
 - South Chahar and North Shansi come from the Japanese map (better fitted,
   about 12 km), so where they meet the atlas-traced Mongol territory the
   Japanese line is kept.
 - Thin strips left between neighbours by tracing error are filled (see the
   "Seam filling" note below), so territories meet each other and the period
   frontier without unassigned slivers.
 - Mengjiang from 1940 is the three 1937-1939 pieces joined; it is not traced
   from a 1940s map.

Usage: python3 combine_territories.py
"""
import json, pickle, sys, numpy as np, cv2
from pyproj import Proj
from scipy.ndimage import distance_transform_edt
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

NC = sys.argv[1] if len(sys.argv) > 1 else 'nc-1935-1940-polys.json'
JP = sys.argv[2] if len(sys.argv) > 2 else 'jp-mengjiang-polys.pkl'
PERIOD = sys.argv[3] if len(sys.argv) > 3 else '../../src/data/period-outlines.json'
NORTH = 'korostovets-1914-north.json'
OUT = sys.argv[4] if len(sys.argv) > 4 else '../../src/data/territories.json'

P = Proj(proj='lcc', lat_1=37, lat_2=47, lat_0=43, lon_0=113, ellps='WGS84')
nc = json.load(open(NC))
def poly(ll): return Polygon([P(a, b) for a, b in ll]).buffer(0)
mmg, ruled, claimed, manchu = [poly(nc[k]) for k in ['mmg', 'ruled', 'claimed', 'manchukuo']]
jp = pickle.load(open(JP, 'rb')); scag, nsag = jp['chanan'], jp['jinbei']

# Outer Mongolia and Russia (with Uriankhai) as Korostovets draws them.
outer = poly(json.load(open(PERIOD))['outer'])
russia = poly(json.load(open(NORTH))['north'])
mpr = unary_union([outer, russia])

def single(g):
    g = g.buffer(0)
    if isinstance(g, MultiPolygon): g = max(g.geoms, key=lambda p: p.area)
    return Polygon(g.exterior)

# South Chahar and North Shansi come from the Japanese map (fitted to about 12 km), so where they meet
# the atlas-traced Mongol territory (about 20-40 km) the Japanese line is kept.
nsag = single(nsag.difference(scag))
south = unary_union([scag, nsag])
ruled = single(ruled.difference(south))
claimed = single(claimed.difference(south))
mmg = single(mmg.difference(south))

# ---- Seam filling -------------------------------------------------------------------------------
# The two traced maps and the MPR guide line each carry their own error, so where two territories
# should meet they leave thin unassigned strips. A strip is filled when it lies between two
# neighbours (the distances to the nearest two add up to no more than `wmax` for that pair) and
# inside the closing of everything drawn (so outer coastlines of a territory are never pushed out).
# Who gets the strip:
#   - Mongol territory vs MPR line or South Chahar / North Shansi: all of it to the Mongol territory.
#   - Mongol territory vs Manchukuo: split down the middle.
#   - Manchukuo vs MPR line, east of 116E: only strips under 15 km, which are within the atlas's own
#     error; wider ones are left, because the border there really did run differently (see the
#     sector note).
RES = 1000.0
minx, miny, maxx, maxy = unary_union([claimed, manchu, south]).buffer(150000).bounds
W, H = int((maxx - minx) / RES) + 1, int((maxy - miny) / RES) + 1
def raster(g):
    m = np.zeros((H, W), np.uint8)
    gs = g.geoms if hasattr(g, 'geoms') else [g]
    for p in gs:
        if p.is_empty: continue
        ext = ((np.array(p.exterior.coords) - [minx, miny]) / RES).round().astype(np.int32)
        cv2.fillPoly(m, [ext], 1)
        for h in p.interiors:
            cv2.fillPoly(m, [((np.array(h.coords) - [minx, miny]) / RES).round().astype(np.int32)], 0)
    return m.astype(bool)
def vector(mask):
    cs, hier = cv2.findContours(mask.astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    out = []
    for c in cs:
        if len(c) < 3: continue
        out.append(Polygon(c[:, 0, :] * RES + [minx, miny]).buffer(0))
    # pixels are cell indices; pad by one cell so the pieces overlap their neighbours, then trim
    return unary_union(out).buffer(RES * 1.5) if out else Polygon()
def dist(mask): return distance_transform_edt(~mask) * RES
def close(mask, r):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * int(r / RES) + 1,) * 2)
    return cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_CLOSE, k).astype(bool)

R = raster(mpr)
def seam(target, others, wmax, closing=50000):
    """Strips between `target` and each of `others` (name -> (mask, wmax_pair)) that should go to target."""
    T = raster(target); dT = dist(T)
    allm = T | R
    for m, _ in others.values(): allm |= m
    C = close(allm, closing) & ~allm
    ds = {k: dist(m) for k, (m, _) in others.items()}
    take = np.zeros_like(T)
    dmin_other = np.minimum.reduce(list(ds.values()))
    for k, (m, w) in others.items():
        # target and k are the two nearest neighbours of the pixel
        pair = (ds[k] <= dmin_other + 1e-6) & (dT + ds[k] <= w)
        take |= pair
    return C & take, dT, ds

# 0. South Chahar against North Shansi: both traced from the same Japanese map, so the hairline strip
#    between them is split down the middle.
A, B = raster(scag), raster(nsag); dA, dB = dist(A), dist(B)
C0 = close(A | B, 15000) & ~(A | B) & (dA + dB <= 20000)
scag = single(unary_union([scag, vector(C0 & (dA <= dB))]))
nsag = single(unary_union([nsag, vector(C0 & (dB < dA))]).difference(scag))
south = unary_union([scag, nsag]).buffer(100).buffer(-100)

# 1. Manchukuo against the MPR line and against all Mongol territory (any year), split at the middle.
G = raster(unary_union([claimed, ruled, mmg, south]))
T = raster(manchu); dT = dist(T); dG = dist(G); dR = dist(R)
allm = T | G | R
C = close(allm, 45000) & ~allm
east = (np.arange(W) * RES + minx)[None, :] >= P(116, 46)[0]
dRu = dist(raster(russia))
m_take = C & (((dT + dG <= 60000) & (dT < dG) & (dG <= dR)) |
              ((dT + dR <= 15000) & (dR < dG) & east) |
              ((dT + dRu <= 30000) & (dRu < dG)))
# Manchukuo meets Russia on Korostovets's line: strips under 30 km are closed, and it is clipped there.
manchu = single(unary_union([manchu, vector(m_take).difference(mpr)]).difference(russia).buffer(-100).buffer(100))

M = raster(manchu); S = raster(south)
def grow(x, neighbours):
    take, _, _ = seam(x, neighbours, None)
    g = unary_union([x, vector(take)])
    g = g.difference(mpr).difference(manchu)
    for n in ('south',):
        if n in neighbours: g = g.difference(south)
    return single(g.buffer(-100).buffer(100))

# Against Outer Mongolia the strips can be wider (up to 100 km): the atlas traced here drew the
# frontier along a later line, and Korostovets's runs up to about 50 km away from it.
ruled = grow(ruled, {'mpr': (R, 100000), 'manchu': (M, 60000), 'south': (S, 90000)})
claimed = grow(unary_union([claimed, ruled]), {'mpr': (R, 100000), 'manchu': (M, 60000), 'south': (S, 90000)})
mmg = grow(mmg, {'mpr': (R, 100000), 'manchu': (M, 60000)})
mj = single(unary_union([ruled, scag, nsag]).buffer(100).buffer(-100))
manchu = single(manchu.difference(unary_union([mj, claimed, mmg])))

out = {}
def ll(g, tol=1500):
    g = g.simplify(tol)
    lon, lat = P(*np.array(g.exterior.coords).T, inverse=True)
    return [[round(float(a), 3), round(float(b), 3)] for a, b in zip(lon, lat)]
# 1940-1945: the part of the 1937 claim that Mengjiang did not rule (chiefly the Ordos). Nakamura (1941)
# draws Mengjiang's state border round the same area, south to the Great Wall.
cl40 = claimed.difference(mj.buffer(500))
cl40 = max(getattr(cl40, 'geoms', [cl40]), key=lambda g: g.area).buffer(-200).buffer(200)
for k, g in [('mmg1936', mmg), ('mlaagRuled', ruled), ('mlaagClaimed', claimed), ('scag', scag),
             ('nsag', nsag), ('mengjiang1939', mj), ('manchukuo', manchu), ('mengjiangClaimed1940', cl40)]:
    out[k] = ll(g); print(k, len(out[k]), round(g.area / 1e6), 'km2')
json.dump(out, open(OUT, 'w'), separators=(',', ':'))
