"""Put Outer Mongolia's frontier with Inner Mongolia and Manchuria back on the
period line, and refit every neighbouring territory to it.

Why: the frontier had been taken from the AoifeIves compilation, whose
“Russian and Mongolian reading” of the 1915 settlement is drawn on the 1962
treaty line. Checked against three period maps, that line is off by 30–60 km
in two sectors, while the period maps agree with one another:
  * 104.5–110.5° E (western Gobi): Korostovets (about 1914) and the Nakamura
    (1941) map agree within about 5–15 km;
  * 116–119.5° E (Shilingol and Hulunbuir sectors): Korostovets and the
    Manchukuo map 滿洲國地圖 (滿洲日報 supplement, 1 January 1934, fitted to its
    own graticule within 2 km) agree within about 10–20 km.
So the MPR's outline is Korostovets's in every year, and changes only where a
source says the frontier moved:
  base      Korostovets, every year to 1941 (his line in the Nomonhan sector runs
            close to the Khalkha River, the line Manchukuo claimed)
  nomonhan  the Khalkhin Gol strip between that line and the MPR's claim line
            (the earlier AoifeIves-based outline), disputed 1935–1941
  mpr1942   base plus the part of the strip on the MPR's side of the 1941
            demarcation (AoifeIves Nomonhan inset, as before)
Neighbours (Hulunbuir 1912, Manchukuo, the Mongol governments, Mengjiang,
Alashan) are cut back where Korostovets's line runs south of the old one, and
extended up to it where it runs north: each strip of land between the old and
the new line goes to whichever neighbour (or none) lies nearest, on a 1 km grid.

Inputs: aoife-outer-mongolia.json and pre-refit-territories.json (the outlines
as they were before this step, kept beside this script), and
../../src/data/period-outlines.json and dariganga-claim.json. Writes
../../src/data/outer-mongolia.json and territories.json. Run
manchukuo_coast.py after it.
"""
import json, numpy as np, cv2
from pyproj import Proj
from scipy.ndimage import distance_transform_edt
from shapely.geometry import Polygon, MultiPolygon, shape, box
from shapely.ops import unary_union

D = '../../src/data/'
P = Proj(proj='lcc', lat_1=37, lat_2=47, lat_0=43, lon_0=113, ellps='WGS84')
O = json.load(open('aoife-outer-mongolia.json')); T = json.load(open('pre-refit-territories.json'))
PO = json.load(open(D + 'period-outlines.json')); DG = json.load(open(D + 'dariganga-claim.json'))

def xy(ring): return Polygon([P(a, b) for a, b in ring]).buffer(0)
def biggest(g):
    g = g.buffer(0)
    if isinstance(g, MultiPolygon): g = max(g.geoms, key=lambda p: p.area)
    return Polygon(g.exterior)
def ll(g, tol=800):
    g = biggest(g).simplify(tol)
    lon, lat = P(*np.array(g.exterior.coords).T, inverse=True)
    return [[round(float(a), 3), round(float(b), 3)] for a, b in zip(lon, lat)]

K = biggest(xy(PO['outer']))

# Frontier with Inner Mongolia, from about 104° E to where Üjümchin meets
# Hulunbuir: the 1930s English banner map (trace_banner_map_1930s.py), which
# draws the Inner Mongolian banner lands whole. It runs within about 5–10 km
# of Korostovets's line for most of its length; west of 104° E (near the
# page's edge) and along Hulunbuir, Korostovets is kept. The two lines are
# joined where they cross near 104° E and where they meet at the Hulunbuir corner.
from shapely.geometry import LineString, Point
from shapely.ops import substring
F30 = json.load(open('frontier-1930s.json'))
Fl = LineString([P(a, b) for a, b in F30['frontier']])
Kb = LineString(K.exterior.coords)
cross = Fl.intersection(Kb)
cands = [g for g in (cross.geoms if hasattr(cross, 'geoms') else [cross]) if not g.is_empty]
cands = [g for g in cands if 103.6 < P(g.x, g.y, inverse=True)[0] < 104.8]
pA = min(cands, key=lambda g: Fl.project(g)) if cands else Fl.interpolate(Fl.project(Kb.interpolate(Kb.project(Point(P(104.2, 41.9))))))
pB = Kb.interpolate(Kb.project(Point(Fl.coords[-1])))
f_seg = substring(Fl, Fl.project(pA), Fl.length)
dA, dB = Kb.project(pA), Kb.project(pB)
north = max(Kb.coords, key=lambda q: q[1]); dN = Kb.project(Point(north))
lo, hi = sorted([dA, dB])
arc = substring(Kb, lo, hi) if lo < dN < hi else LineString(list(substring(Kb, hi, Kb.length).coords) + list(substring(Kb, 0, lo).coords))
arc_coords = list(arc.coords)
if Point(arc_coords[0]).distance(Point(f_seg.coords[-1])) > Point(arc_coords[-1]).distance(Point(f_seg.coords[-1])): arc_coords = arc_coords[::-1]
K = biggest(Polygon(list(f_seg.coords) + arc_coords).buffer(0).buffer(-200).buffer(200))
claim, held_old, m42_old = xy(O['claim']), xy(O['held1935']), xy(O['mpr1942'])
S_old = unary_union([xy(r) for r in O['nomonhan']])

# The Khalkhin Gol strip. Korostovets's line in this sector runs close to the
# Khalkha River, the line Manchukuo claimed, and the old outline's line is the
# MPR's claim line (AoifeIves inset), which the 1941 demarcation largely
# followed. The strip is the land between the two, in the Nomonhan sector only.
NOMONHAN_BOX = box(*P(117.6, 46.4), *P(120.4, 48.25))   # from Buir Nuur south-east
strip = claim.difference(K).intersection(NOMONHAN_BOX).buffer(-1000).buffer(1000)
S = unary_union([p for p in (strip.geoms if hasattr(strip, 'geoms') else [strip]) if p.area > 5e7])

# New MPR outlines.
base = K
held1935 = K
# 1941 demarcation: the whole Manchukuo–MPR frontier was demarcated, so from 1942
# the MPR takes the demarcated line (the earlier outline) along all of it.
FRONTIER_BOX = box(*P(115.3, 46.4), *P(120.4, 50.2))
gain42 = claim.difference(K).intersection(FRONTIER_BOX).intersection(m42_old)
mpr1942 = biggest(unary_union([K, gain42.buffer(1500)]).buffer(3000).buffer(-3000))
nomonhan = S

# Raster grid.
RES = 1000.0
minx, miny, maxx, maxy = K.buffer(400000).bounds
W, H = int((maxx - minx) / RES) + 1, int((maxy - miny) / RES) + 1
def raster(g):
    m = np.zeros((H, W), np.uint8)
    for p in (g.geoms if hasattr(g, 'geoms') else [g]):
        if p.is_empty: continue
        cv2.fillPoly(m, [((np.array(p.exterior.coords) - [minx, miny]) / RES).round().astype(np.int32)], 1)
        for h in p.interiors:
            cv2.fillPoly(m, [((np.array(h.coords) - [minx, miny]) / RES).round().astype(np.int32)], 0)
    return m.astype(bool)
def vector(mask):
    cs, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ps = [Polygon(c[:, 0, :] * RES + [minx, miny]).buffer(0) for c in cs if len(c) >= 3]
    return unary_union(ps) if ps else Polygon()

def refit(new_mpr, old_mpr, neighbours):
    """neighbours: dict name -> polygon (as last fitted to old_mpr). Returns dict of refitted polygons."""
    strip = raster(old_mpr.difference(new_mpr).buffer(1500))
    lab = np.zeros((H, W), np.int16)          # 0 unknown; 1 none; 2.. neighbours
    lab[~raster(new_mpr)] = 1
    names = list(neighbours)
    cut = {n: neighbours[n].difference(new_mpr) for n in names}
    for i, n in enumerate(names):
        lab[raster(cut[n])] = i + 2
    lab[raster(new_mpr)] = 0; lab[strip & ~raster(new_mpr)] = 0
    known = lab > 0
    _, (iy, ix) = distance_transform_edt(~known, return_indices=True)
    nearest = lab[iy, ix]
    out = {}
    for i, n in enumerate(names):
        add = vector(strip & (nearest == i + 2)).buffer(RES)    # overlap slightly, then trim to the frontier
        g = unary_union([cut[n], add.intersection(cut[n].buffer(80000))]).difference(new_mpr)
        out[n] = biggest(g.buffer(600).buffer(-600))
    return out

r = refit(base, claim, {'barga1912': xy(O['barga1912'])}); barga1912 = r['barga1912']
r = refit(base, claim, {'manchukuo1932': xy(T['manchukuo1932']), 'jehol1932': xy(T['jehol1932'])})
manchukuo1932, jehol1932 = r['manchukuo1932'], r['jehol1932']
# 1933–1941: Manchukuo as fitted to the 1935 line; in 1933–1934 it also holds the strip.
r = refit(K.union(S), claim, {'manchukuo': xy(T['manchukuo'])}); manchukuo = r['manchukuo']
manchukuo1933 = biggest(unary_union([manchukuo, nomonhan]).buffer(3000).buffer(-3000).difference(base))
r = refit(mpr1942, m42_old, {'manchukuo1942': xy(T['manchukuo1942']), 'mengjiang1939': xy(T['mengjiang1939'])})
manchukuo1942, mengjiang1939 = r['manchukuo1942'], r['mengjiang1939']
r = refit(base, claim, {'mmg1936': xy(T['mmg1936']), 'manchukuo': manchukuo}); mmg1936 = r['mmg1936']
r = refit(base, claim, {'mmg1937': xy(T['mmg1937']), 'manchukuo': manchukuo}); mmg1937 = r['mmg1937']
ruled, claimed = xy(T['mlaagRuled']), xy(T['mlaagClaimed'])
r = refit(base, claim, {'ruled': ruled, 'claimedOnly': claimed.difference(ruled), 'scag': xy(T['scag']), 'nsag': xy(T['nsag']), 'manchukuo': manchukuo})
mlaagRuled = r['ruled']; mlaagClaimed = biggest(unary_union([r['ruled'], r['claimedOnly']]).buffer(1500).buffer(-1500))
r = refit(base, claim, {'alashan': xy(T['alashan'])}); alashan = r['alashan']
# Mengjiang's claim, 1940–1945: as in combine_territories.py, the 1937 claim less
# the area Mengjiang ruled, recomputed here so that it reaches the same frontier
# as the 1938–1939 claim.
mengjiangClaimed1940 = biggest(mlaagClaimed.difference(mengjiang1939.buffer(500)).buffer(-200).buffer(200))
dariganga = biggest(xy(DG['dariganga'] if 'dariganga' in DG else list(DG.values())[0]).intersection(base))

# Qing Outer Mongolia (to 1911): Khalkha without Dariganga, which until its
# officials petitioned to join Mongolia in March 1912 was an imperial pasture
# under the Chahar administration at Kalgan (Atwood, Encyclopedia of Mongolia,
# 2004, “Dariganga”). The same outline is used for 1921, when Chinese troops
# under Jodbajab held Dariganga from the spring until August.
from shapely.geometry import LineString, Point
dariganga30 = biggest(Polygon([P(a, b) for a, b in F30['dariganga']]).buffer(0).intersection(base))
khalkha = biggest(base.difference(dariganga30.buffer(300)))
russia_lines = unary_union([LineString([P(a, b) for a, b in PO[k]]) for k in ('russiaMongolia', 'tuvaMongolia')]).buffer(8000)
pts = list(khalkha.exterior.coords)
dense = []
for a, b in zip(pts[:-1], pts[1:]):
    n = max(1, int(Point(a).distance(Point(b)) / 1000))
    dense += [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n)]
keep = [not russia_lines.contains(Point(p)) for p in dense]
start = keep.index(False); dense = dense[start:] + dense[:start]; keep = keep[start:] + keep[:start]
runs, cur = [], []
for p, k in zip(dense, keep):
    if k: cur.append(p)
    elif cur: runs.append(cur); cur = []
if cur: runs.append(cur)
runs = [r for r in runs if LineString(r).length > 50000]
def ll_line(r, tol=800):
    lon, lat = P(*np.array(LineString(r).simplify(tol).coords).T, inverse=True)
    return [[round(float(a), 3), round(float(b), 3)] for a, b in zip(lon, lat)]

O2 = {'base': ll(base), 'khalkha': ll(khalkha), 'khalkhaLine': [ll_line(r) for r in runs], 'held1935': ll(held1935), 'mpr1942': ll(mpr1942),
      'nomonhan': [ll(p) for p in (nomonhan.geoms if hasattr(nomonhan, 'geoms') else [nomonhan]) if p.area > 5e7],
      'barga1912': ll(barga1912), 'dariganga': ll(dariganga, 500), 'dariganga1930s': ll(dariganga30, 500)}
json.dump(O2, open(D + 'outer-mongolia.json', 'w'), separators=(',', ':'))
for k, g in [('manchukuo1932', manchukuo1932), ('jehol1932', jehol1932), ('manchukuo1933', manchukuo1933), ('manchukuo', manchukuo),
             ('manchukuo1942', manchukuo1942), ('mengjiang1939', mengjiang1939), ('mmg1936', mmg1936), ('mmg1937', mmg1937),
             ('mlaagRuled', mlaagRuled), ('mlaagClaimed', mlaagClaimed), ('mengjiangClaimed1940', mengjiangClaimed1940), ('alashan', alashan)]:
    T[k] = ll(g)
json.dump(T, open(D + 'territories.json', 'w'), separators=(',', ':'))
for k, v in O2.items(): print(k, len(v))
