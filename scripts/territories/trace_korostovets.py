"""Trace Outer Mongolia (Khalkha) from Korostovets's map of Mongolia.

Source scan: «Карта Монголии, составленная по данным бывшего уполномоченного
в Монголии И. Я. Коростовца, при участии В. Л. Котвича». Издание
Картографического заведения А. Ильина, St Petersburg, about 1914 (scan via
etomesto.com). 2576 x 1878 px. Not stored in the repo.

The map has a printed graticule (every 4 degrees), so it is georeferenced from
the graticule, not from towns:
  - the eight meridians 88-116E were tracked along their whole length and fitted
    as straight lines (rms < 1 px); they meet at an apex, and their angles are
    linear in longitude (residuals < 0.06 deg);
  - the parallels 38-58N are circles about that apex, every 4 deg ~ 364 px.
That is an equidistant conic. Checked on 14 towns, positions fall within about
10-20 km (Urga about 15 km, Kalgan and Peking under 10 km).

Outer Mongolia is the map's orange fill («Халха - Внешняя Монголия»). The fill
is classified by colour (HSV hue 13-20, saturation >= 60), closed over the
lettering and lines, and its outer edge taken.

Russia and Uriankhai (Tuva) share a pale green fill (hue 26-45, saturation
20-65); it is traced the same way and gives the period border with Russia.
The edge of the printed map (its inner neatline) is also written out, since
nothing beyond it is sourced from this map.

Usage: python3 trace_korostovets.py korostovets-mongolia-1914.jpg
Writes korostovets-1914-outer.json, korostovets-1914-north.json and
korostovets-1914-coverage.json (lon/lat rings) beside this script.
"""
import json, sys
import numpy as np, cv2

SCAN = sys.argv[1] if len(sys.argv) > 1 else 'korostovets-mongolia-1914.jpg'

# Graticule model, fitted as described above.
APEX_Y, APEX_X = -4038.35752227, 56.93267073
TA, T0 = 0.69157492, -59.00853047          # angle (deg) = TA * lon + T0
RS, R0 = -91.0, 9478.333333333336           # radius (px) = RS * lat + R0

def to_lonlat(x, y):
    dx, dy = np.asarray(x) - APEX_X, np.asarray(y) - APEX_Y
    t = np.degrees(np.arctan2(dx, dy)); r = np.hypot(dx, dy)
    return (t - T0) / TA, (r - R0) / RS

img = cv2.imread(SCAN)
hsv = cv2.cvtColor(cv2.medianBlur(img, 7), cv2.COLOR_BGR2HSV).astype(int)
H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
mask = ((H >= 13) & (H <= 20) & (S >= 60) & (V >= 180)).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(mask, 8)
mask = (lab == 1 + np.argmax(st[1:, 4])).astype(np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31)))
mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))   # out to the middle of the printed edge
cs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
c = max(cs, key=cv2.contourArea)[:, 0, :].astype(float)
lon, lat = to_lonlat(c[:, 0], c[:, 1])
json.dump({'outer': [[round(float(a), 4), round(float(b), 4)] for a, b in zip(lon, lat)]},
          open('korostovets-1914-outer.json', 'w'), separators=(',', ':'))
print(len(lon), 'points (Outer Mongolia)')

# Russia and Uriankhai, inside the printed map only.
INNER = (102, 86, 2484, 1786)   # x0, y0, x1, y1 of the map inside its neatline, in scan pixels
green = ((H >= 26) & (H <= 45) & (S >= 20) & (S <= 65) & (V >= 170)).astype(np.uint8)
frame = np.zeros_like(green); frame[INNER[1]:INNER[3], INNER[0]:INNER[2]] = 1
green &= frame
green = cv2.morphologyEx(green, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25)))
n, lab, st, _ = cv2.connectedComponentsWithStats(green, 8)
green = (lab == 1 + np.argmax(st[1:, 4])).astype(np.uint8)
cs, _ = cv2.findContours(green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)   # outer edge only: Baikal is filled
c = max(cs, key=cv2.contourArea)[:, 0, :].astype(float)
lon, lat = to_lonlat(c[:, 0], c[:, 1])
json.dump({'north': [[round(float(a), 4), round(float(b), 4)] for a, b in zip(lon, lat)]},
          open('korostovets-1914-north.json', 'w'), separators=(',', ':'))
print(len(lon), 'points (Russia and Uriankhai)')

x0, y0, x1, y1 = INNER
edge = ([(x, y0) for x in np.linspace(x0, x1, 200)] + [(x1, y) for y in np.linspace(y0, y1, 200)] +
        [(x, y1) for x in np.linspace(x1, x0, 200)] + [(x0, y) for y in np.linspace(y1, y0, 200)])
lon, lat = to_lonlat(*np.array(edge).T)
json.dump({'coverage': [[round(float(a), 4), round(float(b), 4)] for a, b in zip(lon, lat)]},
          open('korostovets-1914-coverage.json', 'w'), separators=(',', ':'))
