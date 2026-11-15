"""Write public/map/water.svg: the sea, lakes and rivers of base.svg on a
transparent background, to be laid over the solid territory fills so that
coastlines, lakes and rivers stay visible. Run after make_basemap.py."""
import re
s = open('../../public/map/base.svg').read()
head = re.match(r'<svg[^>]*>', s).group(0)
rect = re.search(r'<rect[^>]*/>', s).group(0)
sea = re.search(r'fill="(#[0-9a-f]{6})"', rect).group(1)
paths = re.findall(r'<path[^>]*/>', s)
land = [p for p in paths if 'fill="#f4f1ea"' in p]
rest = [p for p in paths if 'fill="#f4f1ea"' not in p]
land_d = re.search(r' d="([^"]*)"', land[0]).group(1)
w, h = re.search(r'viewBox="0 0 (\d+) (\d+)"', head).groups()
out = (head + f'<path d="M0 0H{w}V{h}H0Z{land_d}" fill="{sea}" fill-rule="evenodd"/>'
       + land[0].replace('fill="#f4f1ea"', 'fill="none"') + ''.join(rest) + '</svg>')
open('../../public/map/water.svg', 'w').write(out)
print(len(out))
