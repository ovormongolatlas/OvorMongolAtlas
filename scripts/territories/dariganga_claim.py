"""Dariganga as Japanese-era maps claimed it, into src/data/dariganga-claim.json.

Both the Japanese 蒙疆地域圖 (about 1937–1939) and the Nakamura (1941) map draw
Mengjiang's northern border in a loop north of the frontier round Dariganga.
The loop is taken from the Nakamura map (fitted to 24 towns, about 5 km):
Mengjiang's state outline (thickest lines, opened at 21 px on a 4x upscale,
flood-filled and widened 10 km back to the line's middle) is intersected with
Outer Mongolia as Korostovets draws it (period-outlines.json); thin slivers
under 40 km wide, which are tracing differences along the frontier, are
dropped, leaving the loop.

Run fit_nakamura.py first; needs the scan as nakamura.png beside this script.
"""
import json, numpy as np, cv2
from pyproj import Proj
from shapely.geometry import Polygon, Point
P = Proj(proj='lcc', lat_1=37, lat_2=47, lat_0=43, lon_0=113, ellps='WGS84')
C = np.load('nak_coef.npy')
def feats(p): x, y = p[:, 0] / 100, p[:, 1] / 100; return np.c_[np.ones(len(x)), x, y, x * x, x * y, y * y]
S = 4
g = cv2.cvtColor(cv2.imread('nakamura.png'), cv2.COLOR_BGR2GRAY)
dark = (cv2.resize(g, None, fx=S, fy=S, interpolation=cv2.INTER_CUBIC) < 90).astype(np.uint8)
closed = cv2.morphologyEx(dark, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
state = cv2.morphologyEx(closed, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
state = cv2.dilate(state, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
free = (1 - state).astype(np.uint8); free[:, :2] = free[:, -2:] = 0; free[:2, :] = free[-2:, :] = 0
n, lab = cv2.connectedComponents(free, 4)
reg = (lab == lab[int(410 * S), int(230 * S)]).astype(np.uint8)   # seed at Dongsheng
cs, _ = cv2.findContours(reg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
c = max(cs, key=cv2.contourArea)[:, 0, :].astype(float) / S
mj = Polygon(feats(c) @ C).buffer(10000).buffer(0)
outer = Polygon([P(a, b) for a, b in json.load(open('../../src/data/period-outlines.json'))['outer']]).buffer(0)
d = mj.intersection(outer).buffer(-4000).buffer(4000)
d = [p for p in getattr(d, 'geoms', [d]) if p.contains(Point(P(113.85, 45.31)))][0]
o = d.buffer(-20000).buffer(20000)
o = max(getattr(o, 'geoms', [o]), key=lambda q: q.area).buffer(3000).intersection(d).buffer(-200).buffer(200)
o = max(getattr(o, 'geoms', [o]), key=lambda q: q.area).simplify(1500)
lon, lat = P(*np.array(o.exterior.coords).T, inverse=True)
json.dump({'dariganga': [[round(float(a), 3), round(float(b), 3)] for a, b in zip(lon, lat)]},
          open('../../src/data/dariganga-claim.json', 'w'), separators=(',', ':'))
print(round(o.area / 1e6), 'km2')
