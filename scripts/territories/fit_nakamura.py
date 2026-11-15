"""Fit the Nakamura (1941) Mengjiang map to town positions.

Source: “Mengjiang” map, “Source: Nakamura (1941)”, cartography by Harald
Krähe: a modern redraw of a 1941 Japanese map (held privately as
`english mengjiang map.png`; in copyright, traced from only, never published).
Fitted with a quadratic transform to 24 towns; leave-one-out error is about
5 km at the median (worst: Yinchuan 19 km, Baotou 17 km).

Usage: python3 fit_nakamura.py   (writes nak_coef.npy beside this script)
"""
import numpy as np, json
from pyproj import Proj
P=Proj(proj='lcc',lat_1=37,lat_2=47,lat_0=43,lon_0=113,ellps='WGS84')
CP={'Ulaanbaatar':((144.7,23.7),(106.92,47.92)),'Erenhot':((304,228),(111.98,43.65)),'Xilinhot':((440,210),(116.08,43.94)),
'Linxi':((506.3,222.7),(118.05,43.6)),'Chifeng':((541.7,284),(118.96,42.27)),'Chengde':((509,346.7),(117.93,40.97)),
'Dehua':((372.3,307.5),(114.0,41.9)),'Zhangbei':((397.7,342.7),(114.71,41.16)),'Jining':((341.7,348.3),(113.10,41.03)),
'Datong':((347.3,390.7),(113.30,40.09)),'Xuanhua':((411.3,366.7),(115.05,40.61)),'Zhangjiakou':((405.3,358.3),(114.88,40.82)),
'Beijing':((457.3,400),(116.40,39.91)),'Tianjin':((487.3,433.3),(117.20,39.13)),'Baoding':((429.3,447.7),(115.47,38.87)),
'Taiyuan':((322.7,495),(112.55,37.87)),'Jinan':((485.3,550),(117.0,36.65)),'Qingdao':((613.3,566.7),(120.38,36.07)),
'Yinchuan':((97.3,461),(106.27,38.47)),'Dongsheng':((230,403.3),(109.98,39.82)),'Baotou':((228.3,366),(110.05,40.59)),
'Hohhot':((291.7,357.3),(111.66,40.82)),'Yanan':((209,555),(109.49,36.6)),'Bailingmiao':((247,320.5),(110.435,41.70))}
names=list(CP); px=np.array([CP[n][0] for n in names]); XY=np.array([P(*CP[n][1]) for n in names])
def feats(p): x,y=p[:,0]/100,p[:,1]/100; return np.c_[np.ones(len(x)),x,y,x*x,x*y,y*y]
def fit(idx): return np.linalg.lstsq(feats(px[idx]),XY[idx],rcond=None)[0]
C=fit(np.arange(len(names)))
r=np.hypot(*(feats(px)@C-XY).T)/1000
loo=[np.hypot(*(feats(px[i:i+1])@fit([j for j in range(len(names)) if j!=i])-XY[i])[0])/1000 for i in range(len(names))]
for n,a,b in zip(names,r,loo): print(f'{n:12s} fit {a:5.1f}  loo {b:5.1f}')
print('median loo',np.median(loo))
np.save('nak_coef.npy',C)
