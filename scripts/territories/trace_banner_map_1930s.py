"""Trace Outer Mongolia's frontier with Inner Mongolia, and the Dariganga
district, from the English 1930s banner map (`mapofmongols1930s.png`, a
two-page book map of Inner and Outer Mongolia with named banners; source book
not yet identified). Only its right-hand page is used (about 101.8–125° E).

Georeferencing, in two steps:
  1. the page's printed graticule: the meridians 104–124° E (traced as straight
     lines) meet at the cone's apex, and the 42° and 46° N parallels where they
     reach the right-hand neatline give the latitude scale (equidistant conic);
  2. towns drawn on the page (Peking, Dolonnor, Jehol, Mukden, Hsinking, Paotow,
     Tatung) sit about 25 km north of where that grid puts them, so an affine
     correction fitted to those seven towns is applied. Fit residuals 4–15 km,
     leave-one-out 10–26 km.
Lines: the frontier is the map's dash-dot line between Outer Mongolia and the
Inner Mongolian banners (Urat, Muminggan and Dörben Keüked of Ulanchab; the
Sunid, Abaga, Abaganar and Üjümchin banners of Shilingol), from where it enters
the page in the west to where Üjümchin meets Hulunbuir. Dariganga is the
dotted district north of the frontier labelled “Darigangga”. Both are followed
pixel by pixel along the drawn line (least-cost path through dark pixels)
between hand-placed waypoints.

Usage: python3 trace_banner_map_1930s.py mapofmongols1930s.png
Writes frontier-1930s.json beside this script.
"""
import sys, json, numpy as np
from PIL import Image
from scipy.optimize import least_squares
from skimage.graph import route_through_array
from shapely.geometry import LineString, Polygon

im = np.asarray(Image.open(sys.argv[1] if len(sys.argv) > 1 else 'mapofmongols1930s.png').convert('L')).astype(float)

# 1. Graticule.
MER = {104: ((950, 391), (1127, 1199)), 108: ((1019, 64), (1334, 1198)), 112: ((1170, 64), (1467, 971)),
       116: ((1329, 66), (1699, 1051)), 120: ((1515, 130), (1942, 1137)), 124: ((1712, 192), (1937, 665))}
A, b = [], []
for p, q in MER.values():
    p, q = np.array(p, float), np.array(q, float); d = (q - p) / np.linalg.norm(q - p); n = np.array([-d[1], d[0]])
    A.append(n); b.append(n @ p)
apex = np.linalg.lstsq(np.array(A), np.array(b), rcond=None)[0]
Ls = np.array(list(MER)); th = np.array([np.degrees(np.arctan2(*(np.array(q, float) - apex))) for _, q in MER.values()])
k, c = np.polyfit(Ls, th, 1)
r46, r42 = np.hypot(*(np.array([1948, 196]) - apex)), np.hypot(*(np.array([1948, 467]) - apex))
bscale = (r42 - r46) / 4; a0 = r46 + bscale * 46
def fwd(lon, lat):
    t = np.radians(k * lon + c); rho = a0 - bscale * lat
    return apex + rho * np.array([np.sin(t), np.cos(t)])
def grid_inv(x, y): return least_squares(lambda q: fwd(*q) - [x, y], [112, 43]).x

# 2. Town correction.
TOWNS = {'Peking': ((1608, 739.5), (116.40, 39.91)), 'Dolonnor': ((1554.5, 606.5), (116.48, 42.20)),
         'Mukden': ((1845.8, 524.5), (123.43, 41.80)), 'Hsinking': ((1868, 371), (125.32, 43.88)),
         'Jehol': ((1640.8, 663.8), (117.93, 40.97)), 'Paotow': ((1312.7, 793.3), (109.84, 40.65)),
         'Tatung': ((1460.7, 777.3), (113.30, 40.09))}
G = np.array([grid_inv(*v[0]) for v in TOWNS.values()]); R = np.array([v[1] for v in TOWNS.values()])
M = np.linalg.lstsq(np.c_[G, np.ones(len(G))], R, rcond=None)[0]
def to_ll(pts): return np.c_[np.array([grid_inv(x, y) for x, y in pts]), np.ones(len(pts))] @ M

# Least-cost path along the drawn line between waypoints.
cost = 1 + 40 * (im > 150)
def follow(way):
    path = []
    for (x0, y0), (x1, y1) in zip(way[:-1], way[1:]):
        p, _ = route_through_array(cost, (int(y0), int(x0)), (int(y1), int(x1)), fully_connected=True, geometric=True)
        path += [(x, y) for y, x in (p if not path else p[1:])]
    return path

FRONTIER = [(946, 780), (985, 792), (1040, 778), (1070, 760), (1100, 745), (1120, 725), (1140, 695), (1160, 680),
            (1200, 694), (1240, 689), (1250, 687), (1263, 657), (1273, 638), (1303, 625), (1317, 610), (1323, 597),
            (1317, 547), (1330, 533), (1343, 520), (1357, 512), (1370, 503), (1397, 480), (1430, 453), (1463, 423),
            (1490, 400), (1523, 380), (1530, 357), (1553, 347), (1567, 337), (1577, 320), (1582, 290)]
DARIGANGA = [(1313, 490), (1310, 457), (1327, 443), (1327, 417), (1340, 413), (1370, 417), (1403, 420),
             (1417, 427), (1423, 443), (1430, 453)]

def simplify(ll, tol=0.01):
    return [[round(float(x), 3), round(float(y), 3)] for x, y in LineString(ll).simplify(tol).coords]
fr_px = follow(FRONTIER)
fr = to_ll(fr_px[::2] + [fr_px[-1]])
dg_px = follow(DARIGANGA)
dg_line = to_ll(dg_px[::2] + [dg_px[-1]])
# Dariganga: its dotted outline, closed along the frontier between the two junctions.
fl = LineString(fr)
d_start, d_end = fl.project(LineString(dg_line).boundary.geoms[0]), fl.project(LineString(dg_line).boundary.geoms[1])
seg = [fl.interpolate(d).coords[0] for d in np.linspace(d_end, d_start, 60)]   # back along the frontier
dar = Polygon(list(map(tuple, dg_line)) + seg).buffer(0)
if dar.geom_type == 'MultiPolygon': dar = max(dar.geoms, key=lambda p: p.area)
out = {'frontier': simplify(fr), 'dariganga': [[round(x, 3), round(y, 3)] for x, y in dar.exterior.simplify(0.008).coords]}
json.dump(out, open('frontier-1930s.json', 'w'), separators=(',', ':'))
print('frontier', len(out['frontier']), out['frontier'][0], '->', out['frontier'][-1]); print('dariganga', len(out['dariganga']), round(dar.area * 111 * 80), 'km2 approx')
