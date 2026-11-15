"""Add Uriankhai (Tuva) to the Qing outline.

period_outlines.py takes Russia from Korostovets's map, whose Russian fill
includes Uriankhai, a Russian protectorate from 1914. Under the Qing to 1911
Uriankhai was part of Qing Mongolia, so the land north of the Mongolia–Tuva
line (period-outlines.json, `tuvaMongolia`) is added to the `qing` ring. Only a
thin strip of it falls inside this map's frame.
"""
import json
from shapely.geometry import Polygon
from shapely.ops import unary_union
D = '../../src/data/period-outlines.json'
po = json.load(open(D))
t = po['tuvaMongolia']
if t[0][0] > t[-1][0]: t = t[::-1]
east = t[-1][0]
uri = Polygon(t + [[east, 53.0], [88.0, 53.0], [88.0, t[0][1]]]).buffer(0)
qing = unary_union([Polygon(po['qing']).buffer(0), uri]).buffer(0.01).buffer(-0.01)
if qing.geom_type == 'MultiPolygon': qing = max(qing.geoms, key=lambda p: p.area)
qing = qing.simplify(0.01)
po['qing'] = [[round(x, 3), round(y, 3)] for x, y in qing.exterior.coords]
json.dump(po, open(D, 'w'), separators=(',', ':'))
print('qing', len(po['qing']), 'points; Tuva line ends at', t[-1])
