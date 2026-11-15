"""Korea and the Kwantung Leased Territory, for territories.json.

Korea: its land border with Manchuria is the Yalu and Tumen rivers, the line
the Qing and Joseon kept and Japan and China confirmed in 1909; it is drawn
along the rivers' courses as Natural Earth gives them (physical data; the
modern line between the two Koreas is dissolved). For 1946–1950 Korea is split
at the 38th parallel, the line of the 1945 Soviet and American occupation zones.

Kwantung: the land south of the boundary traced from the 1934 Manchukuo map
(kwantung-1934-line.json), clipped to the coast.

Usage: python3 korea_kwantung.py ne_50m_land.geojson ne_10m_admin_0_countries.geojson
"""
import sys, json
from shapely.geometry import Polygon, shape, box
from shapely.ops import unary_union
D = '../../src/data/territories.json'
land = unary_union([shape(f['geometry']).buffer(0) for f in json.load(open(sys.argv[1]))['features']
                    if shape(f['geometry']).intersects(box(115, 33, 135, 45))]).intersection(box(115, 33, 135, 45))
korea = unary_union([shape(f['geometry']) for f in json.load(open(sys.argv[2]))['features']
                     if f['properties']['ADMIN'] in ('North Korea', 'South Korea')]).buffer(0.02).buffer(-0.02)
kl = json.load(open('kwantung-1934-line.json'))
kw = Polygon([(121.0, kl[0][1])] + [tuple(p) for p in kl] + [(122.9, kl[-1][1]), (122.9, 38.4), (121.0, 38.4)]).intersection(land)
def biggest(g):
    return max(getattr(g, 'geoms', [g]), key=lambda p: p.area)
def rings(g, tol=0.01):
    """Main ring and the larger islands, as [main, parts]."""
    ps = sorted([p for p in getattr(g, 'geoms', [g]) if p.area > 0.002], key=lambda p: -p.area)
    return [[[round(x, 3), round(y, 3)] for x, y in p.simplify(tol).exterior.coords] for p in ps]
T = json.load(open(D))
T['korea'] = rings(korea)
T['koreaNorth'] = rings(korea.intersection(box(120, 38.0, 132, 44)))
T['koreaSouth'] = rings(korea.intersection(box(120, 33, 132, 38.0)))
T['kwantung'] = rings(kw, 0.005)
json.dump(T, open(D, 'w'), separators=(',', ':'))
for k in ('korea', 'koreaNorth', 'koreaSouth', 'kwantung'): print(k, len(T[k]), 'rings', [len(r) for r in T[k]][:5])
