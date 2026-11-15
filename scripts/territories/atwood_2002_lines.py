"""Boundaries traced from Christopher Atwood's maps in Young Mongols and Vigilantes
in Inner Mongolia's Interregnum Decades, 1911–1931 (Brill, 2002), drawn by "jmh":

- Map 11.1, "Inner Mongolia and Military Campaigns, 1925–1926": the boundaries of the
  special administrative districts of Chahar, Suiyuan and Rehe, and the frontier
  with the Mongolian People's Republic between Üde and Süli-yin Kheere.
- Map 21.1, "Hulun Buir and the Bargu Revolution, 1928": the frontier between
  Hulun Buir and the MPR from the Russian border to Buir Nuur.

Method. Each scan was fitted to towns with known positions by an affine fit in the
atlas's Lambert conformal conic projection (Map 11.1: 49 towns, leave-one-out error
median 4.5 km, worst 19 km at Baotou; Map 21.1: 10 towns and the two lakes,
median 8 km, worst 18 km). The scan was then warped onto the base map at 3× (Map
11.1) or 4× (Map 21.1) and the dashed lines were read off point by point from the
warped image. Coordinates below are in those warped images' pixels:
  Map 11.1: base px = 570 + x/3, 450 + y/3
  Map 21.1: base px = 962 + x/4,  80 + y/4
The book is in copyright; the scans are not kept in the repository and only the
traced lines are used. Writes atwood-2002-lines.json beside this script.
"""
import json, sys
import numpy as np
from pyproj import Proj

P = Proj(proj='lcc', lat_1=37, lat_2=47, lat_0=43, lon_0=113, ellps='WGS84')
XMIN = P(96.0, 44)[0]; XMAX = P(127.8, 44)[0]; YMAX = P(113, 51.6)[1]; YMIN = P(113, 35.3)[1]
W = 1600; H = round((YMAX - YMIN) * W / (XMAX - XMIN))

def ll(px, py):
    x = XMIN + px / W * (XMAX - XMIN); y = YMAX - py / H * (YMAX - YMIN)
    lon, lat = P(x, y, inverse=True)
    return [round(float(lon), 3), round(float(lat), 3)]

def m11(pts): return [ll(570 + x / 3, 450 + y / 3) for x, y in pts]
def m21(pts): return [ll(962 + x / 4, 80 + y / 4) for x, y in pts]

lines = {
    # Map 11.1, 1925–26
    'chahar-suiyuan': m11([(630, 350), (647.5, 375), (655, 400), (680, 425), (700, 455), (720, 475), (725, 505),
        (740, 540), (747.5, 580), (765, 595), (795, 605), (810, 625), (812.5, 650), (825, 675), (835, 695),
        (815, 710), (790, 725), (775, 740), (755, 732.5), (735, 750), (720, 770), (702.5, 790), (697.5, 815),
        (690, 835), (675, 850), (690, 870), (705, 890), (712.5, 910), (700, 935), (687.5, 965), (682.5, 995),
        (715, 1020), (737.5, 1040), (750, 1047.5)]),
    'chahar-rehe': m11([(1772.5, 42.5), (1767.5, 70), (1760, 105), (1740, 125), (1710, 140), (1680, 155),
        (1650, 175), (1620, 200), (1595, 220), (1570, 230), (1540, 222.5), (1510, 217.5), (1485, 222.5),
        (1467.5, 245), (1457.5, 270), (1477.5, 295), (1475, 310), (1450, 330), (1425, 350), (1410, 375),
        (1405, 400), (1375, 430), (1385, 460), (1410, 480), (1425, 505), (1430, 530), (1440, 555), (1455, 570),
        (1462.5, 595), (1465, 615), (1465, 650), (1462.5, 680), (1445, 685), (1425, 680), (1410, 675),
        (1395, 670), (1375, 672.5), (1365, 685), (1355, 702.5), (1345, 705)]),
    'chahar-zhili': m11([(1345, 705), (1332.5, 735), (1325, 770), (1335, 800), (1330, 840), (1332.5, 870), (1340, 900)]),
    'rehe-fengtian': m11([(2065, 7.5), (2095, 30), (2120, 60), (2137.5, 85), (2125, 102.5), (2095, 120), (2090, 145),
        (2110, 165), (2140, 175), (2147.5, 200), (2160, 215), (2180, 225), (2195, 240), (2200, 270),
        (2192.5, 300), (2185, 320), (2165, 340), (2165, 360), (2187.5, 380), (2205, 400), (2230, 405),
        (2235, 425), (2255, 430), (2270, 445), (2290, 465), (2300, 450), (2295, 430), (2320, 430), (2350, 440),
        (2380, 470), (2375, 500), (2380, 525), (2370, 550), (2345, 565), (2320, 580), (2285, 600), (2260, 625),
        (2245, 645), (2220, 655), (2195, 665), (2170, 680), (2140, 690), (2110, 710), (2100, 730),
        (2102.5, 750), (2087.5, 770), (2085, 790), (2072.5, 805), (2060, 830), (2047.5, 845), (2030, 847.5),
        (2015, 860), (2020, 880), (2015, 895), (1995, 910), (1975, 925), (1955, 945), (1935, 965), (1920, 975),
        (1915, 990), (1917.5, 1000)]),
    'mpr-ude': m11([(631, 185), (650, 215), (680, 240), (697.5, 260), (705, 290), (700, 305), (675, 315),
        (650, 335), (630, 350), (600, 360), (570, 370), (545, 385), (525, 415), (500, 440), (485, 470),
        (460, 490), (435, 505), (395, 517.5), (365, 522.5), (330, 537.5), (300, 550), (270, 557.5)]),
    # Map 21.1, 1928
    'mpr-hulunbuir': m21([(250, 167.5), (240, 220), (225, 265), (210, 310), (195, 355), (175, 400), (155, 440),
        (147.5, 470), (135, 500), (115, 525), (105, 550), (105, 617.5), (90, 640), (65, 655), (60, 670),
        (65, 700), (80, 740), (110, 770), (145, 790), (165, 765), (200, 735), (240, 740), (265, 730),
        (300, 722.5), (330, 727.5), (360, 745), (390, 775), (410, 787.5), (432.5, 755)]),
}
out = sys.argv[1] if len(sys.argv) > 1 else 'atwood-2002-lines.json'
json.dump(lines, open(out, 'w'))
for k, v in lines.items(): print(k, len(v), v[0], v[-1])
