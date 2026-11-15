"""Extend the Russia–Manchuria border east of the point where Korostovets's map
stops (near Blagoveshchensk), along the Amur to the edge of this map's frame.

Source: AoifeIves, “Territorial Changes along the Sino-Russian Border
(1689–2023), Map 1 (of 3): Eastern Border Section” (7000 x 4000 px, EPSG:4326),
its Treaty of Aigun (1858) border line (orange). Georeferenced with an affine fit
to 11 town dots; residuals under 6 km. Run after period_outlines.py.

Usage: python3 extend_amur.py eastern.png
"""
import sys, json, numpy as np, networkx as nx
from PIL import Image
from scipy.spatial import cKDTree
Image.MAX_IMAGE_PIXELS = None
TOWNS = {  # pixel centre of the town dot, (lon, lat)
    'Hailar': ((981.7, 1788.2), (119.77, 49.21)), 'Harbin': ((2305.0, 2454.8), (126.64, 45.76)),
    'Changchun': ((2068.8, 2828.5), (125.32, 43.88)), 'Shenyang': ((1700.3, 3234.7), (123.43, 41.80)),
    'Beijing': ((327.9, 3604.6), (116.40, 39.90)), 'Tianjin': ((484.9, 3764.9), (117.20, 39.13)),
    'Chifeng': ((825.5, 3141.3), (118.89, 42.26)), 'Tongliao': ((1470.5, 2880.0), (122.26, 43.62)),
    'Jinzhou': ((1249.9, 3370.0), (121.13, 41.10)), 'Suihua': ((2389.3, 2288.9), (126.97, 46.65)),
    'Tangshan': ((675.6, 3658.5), (118.18, 39.63)),
}
src = np.array([v[0] for v in TOWNS.values()]); dst = np.array([v[1] for v in TOWNS.values()])
M, *_ = np.linalg.lstsq(np.c_[src, np.ones(len(src))], dst, rcond=None)
A, b = M[:2].T, M[2]
px = lambda lon, lat: np.linalg.solve(A, np.array([lon, lat]) - b)
X0, Y0 = px(127.0, 50.8).astype(int); X1, Y1 = px(130.6, 48.6).astype(int)
a = np.asarray(Image.open(sys.argv[1] if len(sys.argv) > 1 else 'eastern.png').convert('RGB'))[Y0:Y1, X0:X1].astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
m = (R > 165) & (G > 125) & (G < 180) & (B > 55) & (B < 115) & (R - B > 70)   # the orange Aigun line
m[0:215, 150:215] = False; m[0:108, 115:215] = False   # dashed outline of the Sixty-Four Villages claim
ys, xs = np.nonzero(m); pts = np.c_[xs, ys].astype(float)
_, idx = np.unique((pts // 3).astype(int), axis=0, return_index=True); pts = pts[idx]
G2 = nx.Graph()
for i, j in cKDTree(pts).query_pairs(12): G2.add_edge(i, j, weight=float(np.hypot(*(pts[i] - pts[j]))))
T = nx.minimum_spanning_tree(G2.subgraph(max(nx.connected_components(G2), key=len)))
d = nx.single_source_dijkstra_path_length(T, next(iter(T.nodes))); e1 = max(d, key=d.get)
d2, paths = nx.single_source_dijkstra(T, e1); e2 = max(d2, key=d2.get)
ll = np.c_[pts[paths[e2]] + [X0, Y0], np.ones(len(paths[e2]))] @ M
if ll[0, 0] > ll[-1, 0]: ll = ll[::-1]
PATH = '../../src/data/period-outlines.json'
po = json.load(open(PATH)); line = po['russiaManchuria']
end = line[-1]
# Join where the traced Amur first passes south of Korostovets's last point.
k = next(i for i, (x, y) in enumerate(ll) if y < end[1] and x > end[0])
ext = [[round(float(x), 3), round(float(y), 3)] for x, y in ll[k::4] if x < 129.9]
po['russiaManchuria'] = line + ext
json.dump(po, open(PATH, 'w'), separators=(',', ':'))
print('appended', len(ext), 'points', ext[0], '->', ext[-1])
