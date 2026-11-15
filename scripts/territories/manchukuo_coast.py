"""Carry Manchukuo out to the coast, the Yalu and the Kwantung boundary.

Manchukuo's outlines were traced from a small-scale atlas map, so along the
south Manchurian coast and the Korean border they fell short of the coastline
or ran across the Yalu. In the south-east of the map (east of 120.6° E, south of
42.8° N) each outline is grown out to the land and then cut back by:
  * Korea, whose border with Manchuria is the Yalu and Tumen rivers (Natural
    Earth, physical course of the rivers, as for the Qing outline);
  * the Kwantung Leased Territory, Japanese and not part of Manchukuo, whose
    northern boundary is traced from 滿洲國地圖 (滿洲日報 supplement, 1 January
    1934), fitted to 8 towns and a graticule crossing near Liaodong with an
    affine fit (residuals under 4 km): kwantung-1934-line.json;
  * for 1932, Jehol, then a claim (drawn separately).

Usage: python3 manchukuo_coast.py ne_50m_land.geojson ne_10m_admin_0_countries.geojson
"""
import sys, json, numpy as np
from pyproj import Proj
from shapely.geometry import Polygon, MultiPolygon, shape, box
from shapely.ops import unary_union
D = '../../src/data/'
P = Proj(proj='lcc', lat_1=37, lat_2=47, lat_0=43, lon_0=113, ellps='WGS84')
def xy(ring): return Polygon([P(a, b) for a, b in ring]).buffer(0)
def proj(g):
    out = []
    for p in (g.geoms if hasattr(g, 'geoms') else [g]):
        if p.bounds[2] < 115 or p.bounds[0] > 135 or p.bounds[3] < 35 or p.bounds[1] > 50: continue
        out.append(Polygon([P(x, y) for x, y in p.exterior.coords]).buffer(0))
    return unary_union(out)
def biggest(g):
    if isinstance(g, MultiPolygon): g = max(g.geoms, key=lambda p: p.area)
    return Polygon(g.exterior)
def ll(g, tol=800):
    lon, lat = P(*np.array(biggest(g).simplify(tol).exterior.coords).T, inverse=True)
    return [[round(float(a), 3), round(float(b), 3)] for a, b in zip(lon, lat)]

land = unary_union([proj(shape(f['geometry'])) for f in json.load(open(sys.argv[1]))['features']])
countries = {f['properties']['ADMIN']: shape(f['geometry']) for f in json.load(open(sys.argv[2]))['features']
             if f['properties']['ADMIN'] in ('North Korea', 'South Korea', 'Russia')}
korea = unary_union([proj(countries['North Korea']), proj(countries['South Korea'])])
russia = proj(countries['Russia'])
kl = json.load(open('kwantung-1934-line.json'))
kwantung = Polygon([P(*p) for p in [(121.0, kl[0][1])] + kl + [(122.9, kl[-1][1]), (122.9, 38.4), (121.0, 38.4)]]).intersection(land)
SE = Polygon([P(x, y) for x, y in [(120.6, 37.5), (131, 37.5), (131, 42.8), (120.6, 42.8)]])

T = json.load(open(D + 'territories.json'))
for k in ('manchukuo1932', 'manchukuo1933', 'manchukuo', 'manchukuo1942'):
    X = xy(T[k])
    grown = X.buffer(40000).intersection(land).intersection(SE)
    se = unary_union([X.intersection(SE), grown]).intersection(land)
    se = se.difference(korea).difference(kwantung).difference(russia)
    if k == 'manchukuo1932': se = se.difference(xy(T['jehol1932']))
    new = unary_union([X.difference(SE), se]).buffer(300).buffer(-300)
    T[k] = ll(new, 600)
    print(k, round(X.area / 1e6), '->', round(biggest(new).area / 1e6), 'km2')
json.dump(T, open(D + 'territories.json', 'w'), separators=(',', ':'))
