// The base map's vectors, read at build time so pages can draw them inline
// (crisp at any zoom, in every browser) instead of as a scaled <img>/<image>.
import fs from 'node:fs';
import path from 'node:path';

const read = (f: string) => fs.readFileSync(path.join(process.cwd(), 'public/map', f), 'utf8');
// Drops the <svg> wrapper and any <metadata> block (file transfers can stamp one in).
const inner = (svg: string) =>
	svg.replace(/^[\s\S]*?<svg[^>]*>/, '').replace(/<\/svg>\s*$/, '').replace(/<metadata[\s\S]*?<\/metadata>/g, '');

/** Sea, land, rivers and lakes: the whole base map. */
export const baseInner = inner(read('base.svg'));
/** Sea mask, lakes and rivers only, transparent over land: drawn above the territory fills. */
export const waterInner = inner(read('water.svg'));

export const LAND = '#f4f1ea';

/** A solid, opaque colour: the state's colour mixed with the land colour, k = share of the state's colour. */
export const solid = (hex: string, k: number, base = LAND) => {
	const ch = (h: string, i: number) => parseInt(h.slice(i, i + 2), 16);
	return '#' + [1, 3, 5].map((i) => Math.round(ch(hex, i) * k + ch(base, i) * (1 - k)).toString(16).padStart(2, '0')).join('');
};
