"""Regenerate public/map/base.svg, the Timeline Map's physical base map.

The base map is physical only (land, sea, rivers, lakes, graticule). It
deliberately carries no borders and no labels: modern borders would be
anachronistic, and every historical border needs its own source, so borders
and labels are drawn by src/pages/map.astro on top of this image.

Data: Natural Earth (public domain), https://www.naturalearthdata.com
Download these GeoJSON files into the folder you run the script from:
  https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_land.geojson
  https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_lakes.geojson
  https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_rivers_lake_centerlines.geojson

Requires: pip install shapely pyproj
Run:      python make_basemap.py   (writes base.svg; copy it to public/map/)

IMPORTANT: the projection and frame below must stay identical to
src/lib/projection.ts, or the markers drawn by the map page will not line up
with this image.
"""
import json

from pyproj import Proj
from shapely.geometry import LineString, Polygon, box, shape
from shapely.ops import transform, unary_union

# Lambert conformal conic, same parameters as src/lib/projection.ts
P = Proj(proj='lcc', lat_1=37, lat_2=47, lat_0=43, lon_0=113, ellps='WGS84')
x0, _ = P(96.0, 44)
x1, _ = P(127.8, 44)
_, y1 = P(113, 51.6)
_, y0 = P(113, 35.3)
W = 1600
s = W / (x1 - x0)
H = round((y1 - y0) * s)


def proj(x, y, z=None):
    X, Y = P(x, y)
    return ((X - x0) * s, (y1 - Y) * s)


FRAME = box(0, 0, W, H)
CLIP = box(80, 22, 145, 62)  # generous lon/lat window, trimmed to FRAME after projecting


def load(fn, keep=lambda p: True):
    out = []
    for f in json.load(open(fn))['features']:
        if not f['geometry'] or not keep(f['properties']):
            continue
        g = shape(f['geometry'])
        if not g.intersects(CLIP):
            continue
        g = transform(proj, g.intersection(CLIP)).intersection(FRAME)
        if not g.is_empty:
            out.append((f['properties'], g))
    return out


def d_poly(g, tol=0.7):
    g = g.simplify(tol, preserve_topology=True)
    polys = [g] if isinstance(g, Polygon) else [p for p in getattr(g, 'geoms', []) if isinstance(p, Polygon)]
    out = []
    for p in polys:
        for ring in [p.exterior, *p.interiors]:
            c = list(ring.coords)
            if len(c) >= 3:
                out.append('M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in c) + 'Z')
    return ''.join(out)


def d_line(g, tol=0.6):
    g = g.simplify(tol)
    lines = [g] if isinstance(g, LineString) else [l for l in getattr(g, 'geoms', []) if isinstance(l, LineString)]
    return ''.join('M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in l.coords) for l in lines if len(l.coords) > 1)


def rank(p):
    return p.get('scalerank') or 99


land = load('ne_50m_land.geojson')
lakes = load('ne_10m_lakes.geojson', lambda p: rank(p) <= 9)
rivers = load(
    'ne_10m_rivers_lake_centerlines.geojson',
    lambda p: (rank(p) <= 9 and p.get('featurecla', '').startswith('River'))
    or (p.get('featurecla') == 'Lake Centerline' and rank(p) <= 6),
)

graticule = []
for lon in range(90, 141, 5):
    graticule.append(transform(proj, LineString([(lon, la / 2) for la in range(40, 121)])).intersection(FRAME))
for lat in range(30, 61, 5):
    graticule.append(transform(proj, LineString([(lo / 2, lat) for lo in range(170, 291)])).intersection(FRAME))

RIVER_WIDTH = {2: 2.6, 3: 2.8, 4: 2.0, 5: 1.8, 6: 1.7, 7: 1.3, 8: 1.0, 9: 0.8}

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
    f'<rect width="{W}" height="{H}" fill="#cddde6"/>',
    f'<path d="{d_poly(unary_union([g for _, g in land]))}" fill="#f4f1ea" stroke="#a9bfcc" stroke-width="1.2" stroke-linejoin="round"/>',
    f'<path d="{"".join(d_line(g, 0.5) for g in graticule)}" fill="none" stroke="#9aa8b0" stroke-opacity="0.35" stroke-width="0.8"/>',
]
for p, g in sorted(rivers, key=lambda t: -rank(t[0])):
    w = RIVER_WIDTH.get(int(rank(p)), 0.8)
    svg.append(f'<path d="{d_line(g)}" fill="none" stroke="#86adc4" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
svg.append(f'<path d="{d_poly(unary_union([g for _, g in lakes]), 0.5)}" fill="#cddde6" stroke="#86adc4" stroke-width="0.8"/>')
svg.append('</svg>')

open('base.svg', 'w').write('\n'.join(svg))
print(f'wrote base.svg ({W}x{H})')
