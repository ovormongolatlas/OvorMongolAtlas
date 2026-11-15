"""Trace the two readings of the 1915 Kyakhta border from AoifeIves, “Territorial
Changes along the Sino-Russian Border (1689–2023), Map 2 (of 3): Central Border
Section” (7000 x 4000 px; projection EPSG:4326, so longitude and latitude are
linear in the image). Writes kyakhta-1915-readings.json.

Georeferencing: an affine fit to 17 town dots (Irkutsk to Shijiazhuang);
residuals 0.2–5 km. Lines are taken by their legend colours: the Chinese
reading (blue dashed, RGB about 48,88,144) and the Russian and Mongolian
reading (green dashed, about 64,152,40). The magnified Nomonhan inset, drawn in
the same colours, is masked out. Points are chained into one line per reading
(neighbours within 100 px, longest path through the minimum spanning tree).
The green line is mostly drawn underneath the 1962 treaty line; only its
visible pixels are used.

Usage: python3 trace_kyakhta_readings.py central.png
"""
import sys, json, numpy as np, networkx as nx
from PIL import Image
from scipy.spatial import cKDTree
Image.MAX_IMAGE_PIXELS = None
rgb = np.asarray(Image.open(sys.argv[1] if len(sys.argv) > 1 else 'central.png').convert('RGB')).astype(int)
TOWNS = {  # pixel centre of the town dot, (lon, lat)
    'Irkutsk': ((3251.9, 400.0), (104.30, 52.29)), 'Ulaanbaatar': ((3698.6, 1140.4), (106.92, 47.92)),
    'Hailar': ((5871.6, 920.0), (119.77, 49.21)), 'Qiqihar': ((6578.7, 1236.1), (123.92, 47.35)),
    'Daqing': ((6779.5, 1364.1), (125.10, 46.59)), 'Changchun': ((6816.1, 1823.7), (125.32, 43.88)),
    'Chifeng': ((5736.0, 2095.4), (118.89, 42.26)), 'Jinzhou': ((6104.6, 2294.0), (121.13, 41.10)),
    'Shenyang': ((6496.0, 2176.5), (123.43, 41.80)), 'Zhangjiakou': ((5049.0, 2348.5), (114.88, 40.82)),
    'Datong': ((4779.0, 2466.2), (113.30, 40.08)), 'Beijing': ((5303.7, 2497.8), (116.40, 39.90)),
    'Tianjin': ((5440.2, 2636.8), (117.20, 39.13)), 'Tangshan': ((5605.8, 2544.6), (118.18, 39.63)),
    'Yinchuan': ((3582.6, 2740.4), (106.23, 38.49)), 'Yulin': ((4175.0, 2772.3), (109.73, 38.29)),
    'Shijiazhuang': ((4984.9, 2813.4), (114.51, 38.04)),
}
src = np.array([v[0] for v in TOWNS.values()]); dst = np.array([v[1] for v in TOWNS.values()])
A = np.c_[src, np.ones(len(src))]
M, *_ = np.linalg.lstsq(A, dst, rcond=None)
COLOURS = {'chinese': (48, 88, 144), 'mongolian': (64, 152, 40)}
out = {}
for name, c in COLOURS.items():
    mask = np.abs(rgb - np.array(c)).max(2) < 28
    mask[2950:, :] = False; mask[:, :150] = False      # legend and margin
    mask[1430:2010, 5290:] = False                      # the magnified Nomonhan inset
    ys, xs = np.nonzero(mask)
    pts = np.c_[xs, ys].astype(float)
    ll = np.c_[pts, np.ones(len(pts))] @ M
    keep = (ll[:, 0] > 95) & (ll[:, 0] < 121) & (ll[:, 1] > 40) & (ll[:, 1] < 50.5)
    pts, ll = pts[keep], ll[keep]
    # thin to one point per 4 px cell
    _, idx = np.unique((pts // 4).astype(int), axis=0, return_index=True)
    pts, ll = pts[idx], ll[idx]
    G = nx.Graph()
    for i, j in cKDTree(pts).query_pairs(100):
        G.add_edge(i, j, weight=float(np.hypot(*(pts[i] - pts[j]))))
    comp = max(nx.connected_components(G), key=len)
    T = nx.minimum_spanning_tree(G.subgraph(comp))
    a = next(iter(T.nodes)); d = nx.single_source_dijkstra_path_length(T, a); b = max(d, key=d.get)
    d2, paths = nx.single_source_dijkstra(T, b); e = max(d2, key=d2.get)
    line = ll[paths[e]]
    if line[0, 0] > line[-1, 0]: line = line[::-1]
    out[name] = [[round(float(x), 3), round(float(y), 3)] for x, y in line[::3]] + [[round(float(line[-1, 0]), 3), round(float(line[-1, 1]), 3)]]
    print(name, len(comp), 'of', len(pts), 'points chained;', len(out[name]), 'vertices;', out[name][0], '->', out[name][-1])
json.dump(out, open('kyakhta-1915-readings.json', 'w'), separators=(',', ':'))
