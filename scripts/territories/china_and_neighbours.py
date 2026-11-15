"""The Republic of China, the collaborator governments in north China, and the
Jehol–Fengtian provincial line, for territories.json and period-outlines.json.

Run after refit_to_korostovets.py, manchukuo_coast.py, korea_kwantung.py, bogd_1913.py and council_1934.py.

Inputs beside this script:
  east-hebei-1935-40.json      the East Hebei council's area on Narangoa and
      Cribb's 1935–1940 map (same rubber-sheet fit as trace_nc_1935_1940.py).

The Republic of China is drawn as all land in this map's frame that no other
state drawn on the map held in that year: what is left of the Qing outline
after Uriankhai, Korea, the Kwantung Leased Territory and each year's Mongolian,
Manchukuo and Mengjiang areas are taken out. North China under the
Japanese-sponsored governments is drawn by province (see below).

Usage: python3 china_and_neighbours.py ne_50m_land.geojson ne_10m_rivers_lake_centerlines.geojson
"""
import sys, json, numpy as np
from pyproj import Proj
from shapely.geometry import Polygon, MultiPolygon, LineString, shape, box
from shapely.ops import unary_union
D = '../../src/data/'
P = Proj(proj='lcc', lat_1=37, lat_2=47, lat_0=43, lon_0=113, ellps='WGS84')
T = json.load(open(D + 'territories.json')); O = json.load(open(D + 'outer-mongolia.json')); PO = json.load(open(D + 'period-outlines.json'))
def xy(r): return Polygon([P(a, b) for a, b in r]).buffer(0)
def multi(rs): return unary_union([xy(r) for r in rs])
def ll(g, tol=1500):
    g = g.buffer(0)
    ps = sorted([p for p in getattr(g, 'geoms', [g]) if p.area > 3e8], key=lambda p: -p.area)
    out = []
    for p in ps:
        lon, lat = P(*np.array(p.simplify(tol).exterior.coords).T, inverse=True)
        out.append([[round(float(a), 3), round(float(b), 3)] for a, b in zip(lon, lat)])
    return out
land = unary_union([Polygon([P(x, y) for x, y in p.exterior.coords]).buffer(0)
                    for f in json.load(open(sys.argv[1]))['features']
                    for p in getattr(shape(f['geometry']), 'geoms', [shape(f['geometry'])])
                    if p.bounds[0] < 140 and p.bounds[2] > 80 and p.bounds[3] > 25])
qing = xy(PO['qing'])
t = PO['tuvaMongolia']; t = t if t[0][0] < t[-1][0] else t[::-1]
uri = xy(t + [[t[-1][0], 53.0], [88.0, 53.0], [88.0, t[0][1]]])
korea, kw = multi(T['korea']), multi(T['kwantung'])
china = qing.difference(uri).difference(korea.buffer(500)).difference(kw.buffer(300))

M = lambda k: xy(T[k])
mpr, khalkha, mpr42, nom = xy(O['base']), xy(O['khalkha']), xy(O['mpr1942']), multi(O['nomonhan'])
eh = xy(json.load(open('east-hebei-1935-40.json')))
# The council reached the coast: its traced area stops short where the plate's
# lettering covers it, so it is carried south to the coast east of 117.3° E.
eh = unary_union([eh, eh.buffer(25000).intersection(land).intersection(box(*P(117.3, 38.9), *P(119.9, 40.5)))])
eh = eh.difference(M('manchukuo')).buffer(-500).buffer(500)
eh = max(getattr(eh, 'geoms', [eh]), key=lambda p: p.area)

# North China under the Japanese-sponsored governments (1938–1945): the provinces
# the Provisional Government nominally governed, Hebei, Shandong, Shanxi and
# Henan (Boyle 1972, pp. 83–91; Jiangsu lies south of this map), which the North
# China Political Council kept under the Reorganized National Government from
# 1940. Outline: north, Mengjiang and Manchukuo; west, the Yellow River where it
# divides Shanxi from Shaanxi (Natural Earth river course, physical data), then
# south from Tongguan; east, the coast. A sliver of Suiyuan east of the river
# north of 39.75° N, between Mengjiang and the river, is left out.
rivers = [shape(f['geometry']) for f in json.load(open(sys.argv[2]))['features'] if f['properties'].get('name') == 'Huang']
huang = max([g for r in rivers for g in getattr(r, 'geoms', [r])], key=lambda p: p.length)
stretch = list(huang.intersection(box(110.0, 34.4, 111.6, 39.6)).coords)
if stretch[0][1] < stretch[-1][1]: stretch = stretch[::-1]
ring_ll = [(stretch[0][0], 41.2)] + stretch + [(110.3, 33.4), (123.5, 33.4), (123.5, 41.2)]
NCH = Polygon([P(a, b) for a, b in ring_ll]).buffer(0).difference(box(*P(109.0, 39.75), *P(112.2, 42.5)))
def north_china(cut):
    g = NCH.intersection(land).difference(unary_union(cut).buffer(300)).difference(kw.buffer(300))
    return max(getattr(g, 'geoms', [g]), key=lambda p: p.area).buffer(-500).buffer(500)
nc38 = north_china([M('mlaagRuled'), M('scag'), M('nsag'), M('manchukuo')])
nc40 = north_china([M('mengjiang1939'), M('manchukuo'), M('manchukuo1942')])
T['northChina1938'] = ll(nc38); T['northChina1940'] = ll(nc40)

periods = {
    'roc1912': [mpr, xy(O['barga1912'])],
    'roc1913': [mpr, xy(O['barga1912']), M('bogd1913')],
    'roc1916': [mpr],
    'roc1920': [khalkha],   # 1920–1921: Dariganga with China (Chahar), Outer Mongolia on its Qing line
    'roc1932': [mpr, M('manchukuo1932')],
    'roc1933': [mpr, M('manchukuo1933')],
    'roc1934': [mpr, M('manchukuo1933'), multi(T['council1934'])],   # council_1934.py
    'roc1935': [mpr, nom, M('manchukuo'), multi(T['council1935'])],
    'roc1936': [mpr, nom, M('manchukuo'), M('mmg1936'), eh],
    'roc1937': [mpr, nom, M('manchukuo'), M('mmg1937'), eh],
    'roc1938': [mpr, nom, M('manchukuo'), M('mlaagRuled'), M('scag'), M('nsag'), nc38],
    'roc1940': [mpr, nom, M('manchukuo'), M('mengjiang1939'), nc40],
    'roc1942': [mpr42, M('manchukuo1942'), M('mengjiang1939'), nc40],
    'roc1946': [mpr42],
}
FRAME = Polygon([P(x, y) for x, y in [(94, 33.5), (131, 33.5), (131, 51.6), (94, 51.6)]])
for k, cut in periods.items():
    g = china.difference(unary_union(cut).buffer(300))
    # keep the pieces inside this map's frame; drop slivers under 3,000 km² left between traced outlines
    g = unary_union([p for p in getattr(g, 'geoms', [g]) if p.area > 3e9 and p.intersects(FRAME)])
    T[k] = ll(g)
    print(k, [len(r) for r in T[k]], round(max(getattr(g, 'geoms', [g]), key=lambda p: p.area).area / 1e6), 'km2')
T.pop('occupiedChina', None); T['eastHebei'] = ll(eh, 800)
json.dump(T, open(D + 'territories.json', 'w'), separators=(',', ':'))
# Jehol–Fengtian line: the stretch of Jehol's outline (Osaka Asahi, 1932) that runs along Manchukuo's 1932 outline.
j, m = M('jehol1932'), M('manchukuo1932')
seg = j.exterior.intersection(m.buffer(3000))
segs = sorted(getattr(seg, 'geoms', [seg]), key=lambda s: -s.length)
line = segs[0]
lon, lat = P(*np.array(line.simplify(800).coords).T, inverse=True)
PO['jeholFengtian'] = [[round(float(a), 3), round(float(b), 3)] for a, b in zip(lon, lat)]
json.dump(PO, open(D + 'period-outlines.json', 'w'), separators=(',', ':'))
print('jeholFengtian', len(PO['jeholFengtian']), PO['jeholFengtian'][0], PO['jeholFengtian'][-1])
