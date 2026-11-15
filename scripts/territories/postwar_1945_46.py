"""Two short-lived Mongol governments of 1945–1946, for territories.json.

impr1945  The Inner Mongolian People's Republic (provisional government
          proclaimed at Sünid Right Banner, 9 September 1945). Its claimed
          territory is not known from a source in hand. Drawn instead: the
          leagues represented at its founding congress according to the Inner
          Mongolia gazetteer (Shilingol, and seven of the Chahar banners), as
          the Shilingol and Chahar leagues on the Nakamura (1941) map (same fit
          and flood fill as council_1934.py), with the strip up to the Outer
          Mongolian line closed onto them, and the MPR as it stood in 1945
          (Dariganga and the Khalkhin Gol strip included) taken out. The two Chahar banners not
          represented (Plain Blue, Taipusi Left) and the one Ulanchab banner
          that was (Dörben Keüked) are not separable at league scale.

empag1946 The East Mongolian People's Autonomous Government (January–May
          1946), whose provinces were Hinggan, Jirim, Juu Uda, Josotu,
          Hulunbuir and Nawen Muren (Chinese Wikipedia, 東蒙古人民自治政府).
          Drawn as: (a) the eastern Inner Mongolian banner lands of the Jirim,
          Juu Uda and Josotu leagues (the Hinggan banners lay within Jirim) as
          the 1930s English banner map draws their outer boundary, from
          hand-placed points along its dash-dot and dotted lines, converted with
          the same georeference as trace_banner_map_1930s.py (10–26 km); and
          (b) Hulunbuir as outer-mongolia.json `barga1912`. Nawen Muren (the
          Butha banners along the Nonni) has no outline in hand and is not drawn.

Usage: python3 postwar_1945_46.py nakamura.png mapofmongols1930s.png
"""
import sys, json, numpy as np, cv2
from pyproj import Proj
from shapely.geometry import Polygon
from shapely.ops import unary_union
P = Proj(proj='lcc', lat_1=37, lat_2=47, lat_0=43, lon_0=113, ellps='WGS84')
D = '../../src/data/'
O = json.load(open(D + 'outer-mongolia.json')); T = json.load(open(D + 'territories.json'))
xy = lambda r: Polygon([P(a, b) for a, b in r]).buffer(0)
base = xy(O['base'])
# The MPR as it stood in 1945–1946, Dariganga and the Khalkhin Gol strip included.
mpr45 = unary_union([xy(O['mpr1942']), xy(O['dariganga']), base])
def ring_out(g, tol=1500):
    ps = sorted([p for p in getattr(g, 'geoms', [g]) if p.area > 3e9], key=lambda p: -p.area)
    out = []
    for p in ps:
        lon, lat = P(*np.array(p.simplify(tol).exterior.coords).T, inverse=True)
        out.append([[round(float(a), 3), round(float(b), 3)] for a, b in zip(lon, lat)])
    return out

# impr1945: Shilingol and Chahar leagues on the Nakamura map.
exec(open('fit_nakamura.py').read().split("C=fit(np.arange(len(names)))")[0].split('import numpy as np, json')[1].replace("from pyproj import Proj\nP=Proj(proj='lcc',lat_1=37,lat_2=47,lat_0=43,lon_0=113,ellps='WGS84')", ''))
C = fit(np.arange(len(names)))
g = cv2.cvtColor(cv2.imread(sys.argv[1]), cv2.COLOR_BGR2GRAY)
bar = cv2.dilate(cv2.morphologyEx(((g < 110) * 255).astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))), np.ones((2, 2), np.uint8))
polys = []
for seed in [(400, 230), (395, 300)]:   # Shilingol, Chahar
    m = 255 - bar.copy(); cv2.floodFill(m, np.zeros((m.shape[0] + 2, m.shape[1] + 2), np.uint8), seed, 128)
    reg = cv2.dilate((m == 128).astype(np.uint8), np.ones((5, 5), np.uint8))
    c = max(cv2.findContours(reg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0], key=cv2.contourArea)[:, 0, :].astype(float)
    polys.append(Polygon(feats(c) @ C).buffer(0))
L = unary_union(polys).buffer(3000).buffer(-3000)
gap = unary_union([L, base]).buffer(40000).buffer(-40000).difference(base).difference(L)
add = [p for p in getattr(gap, 'geoms', [gap]) if p.distance(L) < 500 and p.distance(base) < 500]
L = unary_union([L] + [p.buffer(300) for p in add]).difference(base).buffer(-300).buffer(300)
T['impr1945'] = ring_out(L.difference(mpr45.buffer(300)).buffer(-500).buffer(500))

# empag1946: eastern banner lands on the 1930s banner map, plus Hulunbuir.
sys.argv = [sys.argv[0], sys.argv[2]]
exec(open('trace_banner_map_1930s.py').read().split('# Least-cost path')[0].split('"""', 2)[2])
EAST = [(1570.7, 443.3), (1575, 423.3), (1585, 410), (1596.7, 398.3), (1606.7, 386.7), (1610, 373.3), (1601.7, 356.7),
        (1590, 336.7), (1581.7, 313.3), (1580, 293.3), (1586.7, 283.3), (1600, 276.7), (1620, 271.7), (1640, 261.7),
        (1660, 255), (1680, 250.7), (1700, 251.7), (1723.3, 251.7), (1731.7, 236.7), (1740, 218.3), (1753.3, 212.7),
        (1773.3, 213.3), (1793.3, 218.3), (1805, 226.7), (1808.3, 243.3), (1820, 251.7), (1833.3, 263.3), (1843.3, 271.7),
        (1860, 286.7), (1873.3, 315), (1865, 333.3), (1860.7, 353.3), (1865, 371.7), (1856.7, 383.3), (1846.7, 406.7),
        (1841.7, 426.7), (1838.3, 456.7), (1831.7, 480), (1826.7, 490), (1813.3, 503.3), (1796.7, 523.3), (1780, 540),
        (1760, 553.3), (1750, 570), (1743.3, 600), (1738.3, 626.7), (1735, 660), (1706.7, 656.7), (1683.3, 653.3),
        (1665, 660), (1655, 672), (1646.7, 653.3), (1640, 640), (1623.3, 626.7), (1618.3, 613.3), (1616.7, 590),
        (1610, 585), (1586.7, 583.3), (1566.7, 588.3), (1543.3, 593.3), (1545, 556.7), (1548.3, 530), (1553.3, 506.7),
        (1561.7, 483.3), (1568.3, 460), (1570, 440)]
east = Polygon([P(*q) for q in to_ll(EAST)]).buffer(0)
E = unary_union([east, xy(O['barga1912'])]).difference(mpr45.buffer(300)).buffer(-500).buffer(500)
T['empag1946'] = ring_out(E)
json.dump(T, open(D + 'territories.json', 'w'), separators=(',', ':'))
for key in ('impr1945', 'empag1946'):
    print(key, [len(r) for r in T[key]])
print('east block bounds', [round(float(v), 2) for v in Polygon(to_ll(EAST)[:, :2]).bounds])
