"""Shilingol and Ulaanchab leagues, held for the Bogd Khanate in 1913.

League outlines from the Nakamura (1941) map's league boundaries in Mengjiang
(the same fit as fit_nakamura.py: quadratic, 24 towns, about 5 km). Shilingol
kept its ten banners from the Qing to the 1940s; Ulaanchab's six banners are
drawn as the Nakamura league, whose southern edge leaves out the counties that
Chinese settlement had carved from it around Hohhot and Baotou (Bayandala in 1941,
under Suiyuan in 1913), and the Hetao plain is cut out (see below).
The strip between the leagues' northern edge and the Outer Mongolian line is
closed onto the leagues. Writes territories.json key `bogd1913`.

Usage: python3 bogd_1913.py nakamura.png ne_10m_rivers_lake_centerlines.geojson
"""
import sys, json, numpy as np, cv2
from pyproj import Proj
from shapely.geometry import Polygon
from shapely.ops import unary_union
P = Proj(proj='lcc', lat_1=37, lat_2=47, lat_0=43, lon_0=113, ellps='WGS84')
exec(open('fit_nakamura.py').read().split("C=fit(np.arange(len(names)))")[0].split('import numpy as np, json')[1].replace("from pyproj import Proj\nP=Proj(proj='lcc',lat_1=37,lat_2=47,lat_0=43,lon_0=113,ellps='WGS84')", ''))
C = fit(np.arange(len(names)))
g = cv2.cvtColor(cv2.imread(sys.argv[1] if len(sys.argv) > 1 else 'nakamura.png'), cv2.COLOR_BGR2GRAY)
lines = cv2.morphologyEx(((g < 110) * 255).astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
bar = cv2.dilate(lines, np.ones((2, 2), np.uint8))
polys = []
for seed in [(400, 230), (200, 300)]:          # Shilingol, Ulaanchab
    m = 255 - bar.copy(); cv2.floodFill(m, np.zeros((m.shape[0] + 2, m.shape[1] + 2), np.uint8), seed, 128)
    reg = cv2.dilate((m == 128).astype(np.uint8), np.ones((5, 5), np.uint8))
    c = max(cv2.findContours(reg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0], key=cv2.contourArea)[:, 0, :].astype(float)
    polys.append(Polygon(feats(c) @ C).buffer(0))
L = unary_union(polys).buffer(3000).buffer(-3000)
O = json.load(open('../../src/data/outer-mongolia.json'))
base = Polygon([P(a, b) for a, b in O['base']]).buffer(0)
gap = unary_union([L, base]).buffer(40000).buffer(-40000).difference(base).difference(L)
add = [p for p in getattr(gap, 'geoms', [gap]) if p.distance(L) < 500 and p.distance(base) < 500]
L = unary_union([L] + [p.buffer(300) for p in add]).difference(base).buffer(-300).buffer(300)
# The Hetao plain, the irrigated farmland of the Chinese counties of Wuyuan and
# Linhe along the Yellow River, is left out: the campaign's bases were on the
# open steppe (Atwood), and its list of places occupied names none of the
# county seats. The plain is approximated, up to the foot of the
# Lang Shan, as the land within 45 km of the Yellow River's northern course
# between 106.8° and 108.9° E (Natural Earth river, physical data); Dashetai,
# north of the Wula Shan at 109.3° E, stays inside.
from shapely.geometry import box, shape, LineString
riv = [shape(f['geometry']) for f in json.load(open(sys.argv[2]))['features'] if f['properties'].get('name') == 'Huang']
huang = max([g for r in riv for g in getattr(r, 'geoms', [r])], key=lambda p: p.length)
north = huang.intersection(box(106.8, 40.0, 108.9, 41.5))
north = unary_union([LineString([P(x, y) for x, y in g.coords]) for g in getattr(north, 'geoms', [north])])
hetao = north.buffer(45000).intersection(box(*P(106.8, 39.0), *P(108.9, 42.0))).buffer(8000).buffer(-8000)
L = L.difference(hetao)
L = max(getattr(L, 'geoms', [L]), key=lambda p: p.area).simplify(1500)
lon, lat = P(*np.array(L.exterior.coords).T, inverse=True)
T = json.load(open('../../src/data/territories.json'))
T['bogd1913'] = [[round(float(a), 3), round(float(b), 3)] for a, b in zip(lon, lat)]
json.dump(T, open('../../src/data/territories.json', 'w'), separators=(',', ':'))
print('bogd1913', len(T['bogd1913']), round(L.area / 1e6), 'km2')
