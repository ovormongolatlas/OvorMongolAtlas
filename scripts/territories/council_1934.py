"""The Mongolian Political Affairs Council's jurisdiction, 1934–1935.

The council was inaugurated at Bat-khaalag (Bailingmiao) on 23 April 1934 with
jurisdiction over ten Shilingol banners, six Ulanchab banners, twelve Chahar
banners and seven Yekejuu banners (Zorigt, "Self-Rule Movement"; see the
council's entry). No map of the council's area has been found, so it is drawn
as the four leagues outlined on the Nakamura (1941) map (the same quadratic fit
as fit_nakamura.py, about 5 km): Shilingol, Ulaanchab, Chahar and Yikezhao.
Limits of that stand-in, recorded in the area's note: the 1941 Chahar league
included Chinese counties (Zhangbei, Dehua) as well as the twelve Chahar
banners, whose lands lay among the counties in 1934; the Yikezhao outline is
the Ordos inside the Great Wall and the Yellow River, Chinese-settled county
land included. As for bogd_1913.py, the Chinese counties around Hohhot and
Baotou (Bayandala in 1941) are outside the leagues, the Hetao plain is cut out
(land within 45 km of the Yellow River's northern course between 106.8° and
108.9° E), and the strip between the leagues and the Outer Mongolian line is
closed onto the leagues.

Writes territories.json keys `council1934` (minus Manchukuo as of 1933–1934)
and `council1935` (minus Manchukuo as of 1935 and the Khalkhin Gol strip).
Run after bogd_1913.py and before china_and_neighbours.py.

Usage: python3 council_1934.py nakamura.png ne_10m_rivers_lake_centerlines.geojson
"""
import sys, json, numpy as np, cv2
from pyproj import Proj
from shapely.geometry import Polygon, box, shape, LineString
from shapely.ops import unary_union
P = Proj(proj='lcc', lat_1=37, lat_2=47, lat_0=43, lon_0=113, ellps='WGS84')
exec(open('fit_nakamura.py').read().split("C=fit(np.arange(len(names)))")[0].split('import numpy as np, json')[1].replace("from pyproj import Proj\nP=Proj(proj='lcc',lat_1=37,lat_2=47,lat_0=43,lon_0=113,ellps='WGS84')", ''))
C = fit(np.arange(len(names)))
g = cv2.cvtColor(cv2.imread(sys.argv[1] if len(sys.argv) > 1 else 'nakamura.png'), cv2.COLOR_BGR2GRAY)
lines = cv2.morphologyEx(((g < 110) * 255).astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
bar = cv2.dilate(lines, np.ones((2, 2), np.uint8))
polys = []
for seed in [(400, 230), (200, 300), (395, 300), (185, 425)]:   # Shilingol, Ulaanchab, Chahar, Yikezhao
    m = 255 - bar.copy(); cv2.floodFill(m, np.zeros((m.shape[0] + 2, m.shape[1] + 2), np.uint8), seed, 128)
    reg = cv2.dilate((m == 128).astype(np.uint8), np.ones((5, 5), np.uint8))
    c = max(cv2.findContours(reg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0], key=cv2.contourArea)[:, 0, :].astype(float)
    polys.append(Polygon(feats(c) @ C).buffer(0))
L = unary_union(polys).buffer(3000).buffer(-3000)
D = '../../src/data/'
O = json.load(open(D + 'outer-mongolia.json')); T = json.load(open(D + 'territories.json'))
xy = lambda r: Polygon([P(a, b) for a, b in r]).buffer(0)
base = xy(O['base'])
gap = unary_union([L, base]).buffer(40000).buffer(-40000).difference(base).difference(L)
add = [p for p in getattr(gap, 'geoms', [gap]) if p.distance(L) < 500 and p.distance(base) < 500]
L = unary_union([L] + [p.buffer(300) for p in add]).difference(base).buffer(-300).buffer(300)
riv = [shape(f['geometry']) for f in json.load(open(sys.argv[2]))['features'] if f['properties'].get('name') == 'Huang']
huang = max([g for r in riv for g in getattr(r, 'geoms', [r])], key=lambda p: p.length)
north = huang.intersection(box(106.8, 40.0, 108.9, 41.5))
north = unary_union([LineString([P(x, y) for x, y in g.coords]) for g in getattr(north, 'geoms', [north])])
hetao = north.buffer(45000).intersection(box(*P(106.8, 39.0), *P(108.9, 42.0))).buffer(8000).buffer(-8000)
L = L.difference(hetao)
nom = unary_union([xy(r) for r in O['nomonhan']])
for key, cut in [('council1934', [xy(T['manchukuo1933'])]), ('council1935', [xy(T['manchukuo']), nom])]:
    G = L.difference(unary_union(cut).buffer(300)).buffer(-500).buffer(500)
    parts = sorted([p for p in getattr(G, 'geoms', [G]) if p.area > 3e9], key=lambda p: -p.area)
    out = []
    for p in parts:
        lon, lat = P(*np.array(p.simplify(1500).exterior.coords).T, inverse=True)
        out.append([[round(float(a), 3), round(float(b), 3)] for a, b in zip(lon, lat)])
    T[key] = out
    print(key, [len(r) for r in out], [round(p.area / 1e6) for p in parts], 'km2')
json.dump(T, open(D + 'territories.json', 'w'), separators=(',', ':'))
