"""Shilingol League's northern and eastern edges, after the period maps that agree.

Two corrections, both in the Üjümüchin banners of north-eastern Shilingol:

1. Frontier with Outer Mongolia, from Dariganga's south-east corner (about
   116.0° E) to the Hulunbuir corner (about 119.7° E). The MPR outline had this
   stretch from the 1930s English banner map (trace_banner_map_1930s.py), whose
   fit is weakest in this corner of its page; it ran 30–80 km south of where
   three other sources put the frontier, giving the northern Üjümüchin lands to
   Mongolia. Nakamura (1941; Harald Krähe's redraw, fitted as fit_nakamura.py),
   Atwood's Map i.1 (Inner Mongolia under the Qing, borders as in 1820) and the
   1962 Sino-Mongolian treaty line agree within about 10–30 km on a line further
   north. No source has the Üjümüchin banners joining the Bogd Khanate or the
   MPR; Atwood (Encyclopedia, "Shiliin Gol", "Üjümüchin") has the Shilingol
   banners submitting to the Republic in 1915. The line is now Nakamura's, read
   from the redraw warped onto the base map (ujumuchin-frontier-nakamura-px.json:
   pixels of that 2× warp of the window 113–121° E, 43.5–48.3° N, whose top-left
   is base-map pixel 854, 233).

2. Border with Manchukuo (and, in 1932, Jehol). Manchukuo had been drawn from
   Narangoa and Cribb's modern atlas, which puts a band of eastern Shilingol
   (roughly 117–120° E) in Manchukuo from 1933. Nakamura (1941), Atwood's Map
   i.1 and his Map 11.1 (1925–1926) put that band inside Shilingol (the
   Shilingol–Juu Uda league line), and the 1930s banner map draws Manchukuo's
   border at the eastern edge of East Üjümüchin. So the band is taken out of
   Manchukuo and Jehol in every year and given to whoever held Shilingol.

3. The East Mongolian People's Autonomous Government (1946), outlined from the
   banner map's Jirim–Juu Uda–Josotu boundary, overlapped the same band by about
   12,000 km²; Shilingol is taken out of it.

The strip in (1) is taken out of every Outer Mongolian outline and added to
every territory that met the old line there; the band in (2) is taken out of the
Manchukuo/Jehol rings and added to the territories that border it. Run after
postwar_1945_46.py (it uses `impr1945` as the Nakamura Shilingol-and-Chahar fill).
"""
import json
import numpy as np
from pyproj import Proj
from shapely.geometry import Polygon, LineString, Point, box, MultiPolygon
from shapely.ops import unary_union, substring, split

P = Proj(proj='lcc', lat_1=37, lat_2=47, lat_0=43, lon_0=113, ellps='WGS84')
D = '../../src/data/'
O = json.load(open(D + 'outer-mongolia.json')); T = json.load(open(D + 'territories.json'))
PO = json.load(open(D + 'period-outlines.json'))

XMIN = P(96.0, 44)[0]; XMAX = P(127.8, 44)[0]; YMAX = P(113, 51.6)[1]; YMIN = P(113, 35.3)[1]
W = 1600; H = round((YMAX - YMIN) * W / (XMAX - XMIN))
def base_px_to_xy(px, py): return (XMIN + px / W * (XMAX - XMIN), YMAX - py / H * (YMAX - YMIN))

def is_ring(v): return isinstance(v[0][0], (int, float))
def rings(v): return [v] if is_ring(v) else v
def poly(v): return unary_union([Polygon([P(*p) for p in r]).buffer(0) for r in rings(v)])
def out(g, like, tol=600):
    ps = sorted([p for p in getattr(g, 'geoms', [g]) if p.area > 3e8], key=lambda p: -p.area)
    res = []
    for p in ps:
        lon, lat = P(*np.array(p.simplify(tol).exterior.coords).T, inverse=True)
        res.append([[round(float(a), 3), round(float(b), 3)] for a, b in zip(lon, lat)])
    return res[0] if (is_ring(like) or len(res) == 1) and len(res) >= 1 and is_ring(like) else res

# (1) New frontier line and the strip between it and the old MPR edge.
px = json.load(open('ujumuchin-frontier-nakamura-px.json'))
new = LineString([base_px_to_xy(854 + x / 2, 233 + y / 2) for x, y in px])
base = poly(O['base'])
ob = LineString(base.exterior.coords)
a, b = Point(new.coords[0]), Point(new.coords[-1])
da, db = ob.project(a), ob.project(b)
lo, hi = sorted([da, db])
arc = substring(ob, lo, hi)
if arc.length > 1.5e6:   # took the long way round
    arc = LineString(list(substring(ob, hi, ob.length).coords) + list(substring(ob, 0, lo).coords))
ac = list(arc.coords)
if Point(ac[0]).distance(a) > Point(ac[-1]).distance(a): ac = ac[::-1]
strip = Polygon([ob.interpolate(da).coords[0]] + list(new.coords) + [ob.interpolate(db).coords[0]] + ac[::-1]).buffer(0)
strip = strip.intersection(base)
keep_mpr = unary_union([poly(O['dariganga']), poly(O['barga1912']), poly(O['nomonhan'])])
strip = strip.difference(keep_mpr)
strip = unary_union([p for p in getattr(strip, 'geoms', [strip]) if p.area > 2e8])
print('frontier strip km2', round(strip.area / 1e6))

# (2) The band: Shilingol (Nakamura fill, plus the strip) inside Manchukuo or Jehol.
shil = unary_union([poly(T['impr1945']), strip])
MK = ['manchukuo1933', 'manchukuo', 'manchukuo1942', 'manchukuo1932', 'jehol1932']
band = unary_union([shil.intersection(poly(T[k])) for k in MK if k in T])
band = unary_union([p for p in getattr(band, 'geoms', [band]) if p.area > 5e9])
print('band km2', round(band.area / 1e6))

MPR_O = ['base', 'khalkha', 'held1935', 'mpr1942']
changed = []
for k in MPR_O:
    g = poly(O[k]); g2 = g.difference(strip.buffer(300))
    if abs(g2.area - g.area) > 1e8: O[k] = out(g2.buffer(0), O[k]); changed.append('outer.' + k)

# Territories that met the old line in the sector get the strip; those that met the band get the band.
sector = box(*P(115.8, 45.3), *P(119.9, 47.0))
old_line = ob.intersection(sector)
for k, v in T.items():
    try: g = poly(v)
    except Exception: continue
    if k in MK:
        g2 = g.difference(band.buffer(300))
    else:
        g2 = g
        if g.boundary.intersection(old_line.buffer(2500)).length > 5e4: g2 = unary_union([g2, strip.buffer(400)])
        if k not in ('impr1945',) and g2.boundary.intersection(band.boundary.buffer(2500)).length > 5e4 and not g2.contains(band.representative_point()):
            g2 = unary_union([g2, band.buffer(400)])
    if abs(g2.area - g.area) > 1e8:
        T[k] = out(g2.buffer(1500).buffer(-1500), v); changed.append(k)

# (3) The East Mongolian government's 1946 outline (from the banner map's Jirim,
# Juu Uda and Josotu boundary) runs into the same band; Shilingol is taken out of it.
if 'empag1946' in T:
    shil2 = poly(T['impr1945'])
    g = poly(T['empag1946']); g2 = g.difference(shil2.buffer(300))
    if abs(g2.area - g.area) > 1e8: T['empag1946'] = out(g2.buffer(1500).buffer(-1500), T['empag1946']); changed.append('empag1946')

# The Qing-era line between Outer Mongolia and the Inner Mongolian leagues.
kl = O['khalkhaLine']
def replace_seg(coords):
    L = LineString([P(*p) for p in coords])
    if L.distance(old_line) > 3000: return coords
    da2, db2 = L.project(a), L.project(b)
    if abs(da2 - db2) < 1e4: return coords
    lo2, hi2 = sorted([da2, db2])
    first = list(substring(L, 0, lo2).coords); last = list(substring(L, hi2, L.length).coords)
    mid = list(new.coords) if da2 < db2 else list(new.coords)[::-1]
    lon, lat = P(*np.array(first + mid + last).T, inverse=True)
    return [[round(float(x), 3), round(float(y), 3)] for x, y in zip(lon, lat)]
O['khalkhaLine'] = [replace_seg(c) for c in kl] if not is_ring(kl) else replace_seg(kl); changed.append('outer.khalkhaLine')

json.dump(O, open(D + 'outer-mongolia.json', 'w'), separators=(',', ':'))
json.dump(T, open(D + 'territories.json', 'w'), separators=(',', ':'))
print('changed', changed)
