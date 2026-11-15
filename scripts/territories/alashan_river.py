"""Close Alashan Banner's eastern edge up to the Yellow River.

The 1930 banner map (蒙古盟旗記位圖) draws the banner's eastern edge along the
Yellow River from the north-east corner near Dengkou (about 40.35° N) down to
where the boundary leaves the river towards the Helan Shan (about 39.15° N).
The hand digitisation of that map (in territories.json, key 'alashan') puts the
river up to about 60 km too far west, as the sketch map is off by up to about
40 km near Ningxia. Along that stretch the edge is therefore drawn on the
river itself (Natural Earth rivers, physical data), as is done for the Yalu.

Usage: python3 alashan_river.py ne_10m_rivers_lake_centerlines.geojson
"""
import sys, json
from shapely.geometry import shape, Polygon, MultiLineString, LineString
from shapely.ops import unary_union, linemerge
N, S = 40.35, 39.15
PATH = '../../src/data/territories.json'
t = json.load(open(PATH)); old = Polygon(t['alashan'])
parts = []
for f in json.load(open(sys.argv[1]))['features']:
    if f['properties'].get('name') == 'Huang':
        g = shape(f['geometry'])
        parts += list(g.geoms) if hasattr(g, 'geoms') else [g]
river = max((p for p in parts if p.bounds[1] < S and p.bounds[3] > N), key=lambda p: p.length)
pts = [(x, y) for x, y in river.coords if S <= y <= N and x < 107.6]
pts.sort(key=lambda q: -q[1])  # north to south
east = [(x, y) for x, y in old.exterior.coords if S <= y <= N and x > 105.0]
east.sort(key=lambda q: q[1])  # south to north
fill = Polygon(pts + east).buffer(0)
new = unary_union([old, fill]).buffer(0.02).buffer(-0.02)
if new.geom_type != 'Polygon': new = max(new.geoms, key=lambda p: p.area)
new = new.simplify(0.01)
t['alashan'] = [[round(x, 3), round(y, 3)] for x, y in new.exterior.coords]
json.dump(t, open(PATH, 'w'), separators=(',', ':'))
print('area before', round(old.area, 3), 'after', round(new.area, 3), len(t['alashan']), 'points')
