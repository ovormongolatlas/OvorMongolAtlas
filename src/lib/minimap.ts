/**
 * Build-time data for the small map on each entry page (src/components/MiniMap.astro).
 *
 * The mini-map is a cropped, static view of the Timeline Map: the same base
 * image, the same territories and the same 1 July rule, frozen at one year.
 * It is drawn entirely at build time so entry pages stay light on old devices;
 * the only interaction is the link through to the full Timeline Map.
 */
import { areas, campaigns, type Area, type AreaKind } from '../data/map-boundaries';
import { referenceTowns } from '../data/map-labels';
import { BASE_MAP_HEIGHT as H, BASE_MAP_WIDTH as W, isOnMap, mapPosition } from './projection';

/** Must match the Timeline Map's slider (src/pages/map.astro). */
export const YEAR_MIN = 1890;
export const YEAR_MAX = 1950;
/** The year the Timeline Map opens on; preferred whenever an entry covers it. */
export const DEFAULT_YEAR = 1938;

export const AREA_KIND_LABEL: Record<AreaKind, string> = {
	ruled: 'Ruled',
	claimed: 'Claimed, not ruled',
	context: 'Other state, for context',
	disputed: 'Disputed',
	occupied: 'Troops present, not annexed',
};

type LonLat = [number, number];
type Box = { x: number; y: number; w: number; h: number };

export interface MiniPoint {
	id?: string;
	name: string;
	lon: number;
	lat: number;
	kind: 'self' | 'linked' | 'town';
	type?: string;
}

export interface MiniMapInput {
	id: string;
	type: string;
	startYear?: number;
	endYear?: number;
	altStartYear?: number;
	altEndYear?: number;
	location?: { lat: number; lon: number };
	title: string;
	/** Places and battles this entry links to, with their own locations. */
	linked: MiniPoint[];
	/** Width the map is laid out for, in CSS pixels; text is sized to match. */
	displayWidth?: number;
}

export interface MiniMapData {
	year?: number;
	displayWidth: number;
	view: Box;
	fontSize: number;
	areas: { d: string; color: string; dark: string; kind: AreaKind; look?: 'zone' | 'blocks'; name: string; own: boolean }[];
	hatchColors: string[];
	points: (MiniPoint & { x: number; y: number; label?: { x: number; y: number; anchor: 'start' | 'end' | 'middle' } })[];
	legend: { name: string; color: string; kind: AreaKind; look?: 'zone' | 'blocks'; own: boolean }[];
	mapHref: string;
	/** The entry's own point, when it is drawn. */
	selfOnMap: boolean;
	/** The entry's own campaign routes, as curves (same shape as on the Timeline Map). */
	routes: string[];
}

const active = (s: { start: number; end: number }, y: number) => y >= s.start && y <= s.end;

export const darker = (hex: string, f = 0.62) =>
	'#' + [1, 3, 5].map((i) => Math.round(parseInt(hex.slice(i, i + 2), 16) * f).toString(16).padStart(2, '0')).join('');

const px = (lon: number, lat: number): [number, number] => {
	const { left, top } = mapPosition(lon, lat);
	return [(left / 100) * W, (top / 100) * H];
};

/** All rings of an area, in base-map pixels. */
function rings(a: Area): [number, number][][] {
	const out = [a.coordinates, ...(a.parts ?? [])];
	if (a.exclude) out.push(a.exclude);
	return out.filter((r) => r.length).map((r) => r.map(([lon, lat]) => px(lon, lat)));
}

function bboxOf(pts: [number, number][]): Box | null {
	if (!pts.length) return null;
	let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
	for (const [x, y] of pts) {
		if (x < x0) x0 = x;
		if (y < y0) y0 = y;
		if (x > x1) x1 = x;
		if (y > y1) y1 = y;
	}
	return { x: x0, y: y0, w: x1 - x0, h: y1 - y0 };
}

const intersects = (a: Box, b: Box) => a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;

/** Path data for one ring, dropping points closer together than `tol` pixels. */
function ringPath(r: [number, number][], tol: number): string {
	const kept: [number, number][] = [r[0]];
	for (let i = 1; i < r.length; i++) {
		const [lx, ly] = kept[kept.length - 1];
		if (Math.hypot(r[i][0] - lx, r[i][1] - ly) >= tol || i === r.length - 1) kept.push(r[i]);
	}
	return kept.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`).join('') + 'Z';
}

/** Unbroken runs of years in which `test` holds, within the map's range. */
function runs(test: (y: number) => boolean) {
	const out: { start: number; end: number }[] = [];
	for (let y = YEAR_MIN; y <= YEAR_MAX; y++) {
		if (!test(y)) continue;
		const last = out.at(-1);
		if (last && last.end === y - 1) last.end = y;
		else out.push({ start: y, end: y });
	}
	return out;
}

/** The year a run of years is best shown at: the default year if it falls inside, else the middle. */
function yearIn(rs: { start: number; end: number }[]): number | undefined {
	if (!rs.length) return undefined;
	const hit = rs.find((r) => active(r, DEFAULT_YEAR));
	if (hit) return DEFAULT_YEAR;
	const longest = rs.reduce((a, b) => (b.end - b.start > a.end - a.start ? b : a));
	return Math.floor((longest.start + longest.end) / 2);
}

export function ownAreas(id: string) {
	return areas.filter((a) => a.entry === id && a.coordinates.length);
}

export function ownCampaigns(id: string) {
	return campaigns.filter((c) => c.entry === id);
}

/** The year an entry's mini-map shows, or undefined when it has none inside the map's range. */
export function pickYear(e: MiniMapInput): number | undefined {
	const own = ownAreas(e.id);
	if (own.length) return yearIn(runs((y) => own.some((a) => active(a, y))));
	const camp = ownCampaigns(e.id);
	if (camp.length) return yearIn(runs((y) => camp.some((c) => active(c, y))));
	if (e.startYear === undefined || e.endYear === undefined) return undefined;
	const start = Math.min(e.startYear, e.altStartYear ?? e.startYear);
	const end = Math.max(e.endYear, e.altEndYear ?? e.endYear);
	return yearIn(runs((y) => y >= start && y <= end));
}

const ASPECT = 3 / 4;

function frame(content: Box, minW: number): Box {
	let w = Math.max(content.w * 1.3, minW);
	let h = Math.max(content.h * 1.3, w * ASPECT);
	w = Math.max(w, h / ASPECT);
	h = w * ASPECT;
	w = Math.min(w, W);
	h = Math.min(h, H);
	let x = content.x + content.w / 2 - w / 2;
	let y = content.y + content.h / 2 - h / 2;
	x = Math.min(Math.max(x, 0), W - w);
	y = Math.min(Math.max(y, 0), H - h);
	return { x, y, w, h };
}

export function buildMiniMap(e: MiniMapInput): MiniMapData | null {
	const year = pickYear(e);
	const own = year === undefined ? [] : ownAreas(e.id).filter((a) => active(a, year));
	const ownCamps = year === undefined ? [] : ownCampaigns(e.id).filter((c) => active(c, year));

	const self: MiniPoint | null =
		e.location && isOnMap(e.location.lon, e.location.lat)
			? { id: e.id, name: e.title, lon: e.location.lon, lat: e.location.lat, kind: 'self', type: e.type }
			: null;
	const linked = e.linked.filter((p) => p.id !== e.id && isOnMap(p.lon, p.lat));

	// What the view must contain: the entry's own territory, else its own point and
	// campaign, else the places it links to.
	const focus: [number, number][] = [];
	own.forEach((a) => rings(a).slice(0, a.exclude ? -1 : undefined).forEach((r) => focus.push(...r)));
	if (self) focus.push(px(self.lon, self.lat));
	ownCamps.forEach((c) => c.routes.forEach((r) => focus.push(px(...r.from), px(...r.to))));
	if (!focus.length) linked.forEach((p) => focus.push(px(p.lon, p.lat)));
	const content = bboxOf(focus);
	if (!content) return null;
	const view = frame(content, own.length || ownCamps.length ? 260 : self && !linked.length ? 520 : 400);
	const displayWidth = e.displayWidth ?? 300;
	const scale = view.w / displayWidth;
	const fontSize = 12.5 * scale;

	// Territories in force on 1 July of the year, culled to the view.
	const KIND_ORDER: Record<string, number> = { context: 0, ruled: 1, occupied: 2, claimed: 3, disputed: 4 };
	// Fills are opaque, so context states go underneath and hatched areas on top.
	const drawn = year === undefined ? [] : areas.filter((a) => a.coordinates.length && active(a, year)).sort((a, b) => (a.look ? 10 : KIND_ORDER[a.kind]) - (b.look ? 10 : KIND_ORDER[b.kind]));
	const tol = scale * 0.8;
	const areaShapes = drawn
		.map((a) => ({ a, rs: rings(a) }))
		.filter(({ rs }) => rs.some((r) => intersects(bboxOf(r)!, view)))
		.map(({ a, rs }) => ({
			d: rs.map((r) => ringPath(r, tol)).join(''),
			color: a.color,
			dark: darker(a.color),
			kind: a.kind,
			look: a.look,
			name: a.legendName ?? a.name,
			own: a.entry === e.id,
		}));

	// Points: the entry itself, then what it links to, then reference towns for bearings.
	const towns: MiniPoint[] =
		year === undefined
			? []
			: referenceTowns
					.filter((t) => active({ start: t.start ?? YEAR_MIN, end: t.end ?? YEAR_MAX }, year))
					.map((t) => ({ name: t.name, lon: t.lon, lat: t.lat, kind: 'town' as const }));
	const inView = (x: number, y: number) => x > view.x && x < view.x + view.w && y > view.y && y < view.y + view.h;
	const all = [...(self ? [self] : []), ...linked, ...towns]
		.map((p) => {
			const [x, y] = px(p.lon, p.lat);
			return { ...p, x, y };
		})
		.filter((p) => inView(p.x, p.y));

	// Names: try right, left, above, below; skip a name that would cover another.
	const placed: Box[] = all.map((p) => ({ x: p.x - 4 * scale, y: p.y - 4 * scale, w: 8 * scale, h: 8 * scale }));
	const inside = (b: Box) => b.x >= view.x + 2 * scale && b.y >= view.y + 2 * scale && b.x + b.w <= view.x + view.w - 2 * scale && b.y + b.h <= view.y + view.h - 2 * scale;
	const points = all.map((p, i) => {
		const fs = p.kind === 'town' ? fontSize * 0.88 : fontSize;
		const tw = p.name.length * fs * (p.kind === 'town' ? 0.52 : 0.58);
		const th = fs * 1.1;
		const gap = (p.kind === 'town' ? 5 : 8) * scale;
		const tries: { box: Box; label: { x: number; y: number; anchor: 'start' | 'end' | 'middle' } }[] = [
			{ box: { x: p.x + gap, y: p.y - th / 2, w: tw, h: th }, label: { x: p.x + gap, y: p.y + fs * 0.35, anchor: 'start' } },
			{ box: { x: p.x - gap - tw, y: p.y - th / 2, w: tw, h: th }, label: { x: p.x - gap, y: p.y + fs * 0.35, anchor: 'end' } },
			{ box: { x: p.x - tw / 2, y: p.y - gap - th, w: tw, h: th }, label: { x: p.x, y: p.y - gap - fs * 0.2, anchor: 'middle' } },
			{ box: { x: p.x - tw / 2, y: p.y + gap, w: tw, h: th }, label: { x: p.x, y: p.y + gap + fs * 0.85, anchor: 'middle' } },
		];
		const others = placed.filter((_, j) => j !== i);
		const ok = tries.find((t) => inside(t.box) && !others.some((b) => intersects(b, t.box)));
		if (!ok) return { ...p };
		placed.push(ok.box);
		return { ...p, label: ok.label };
	});

	const legend = [...new Map(
		[...areaShapes].sort((a, b) => Number(b.own) - Number(a.own)).map((s) => [s.name, { name: s.name, color: s.color, kind: s.kind, look: s.look, own: s.own }]),
	).values()].slice(0, 8);

	const routes = ownCamps.flatMap((c) =>
		c.routes.map((r) => {
			const [x0, y0] = px(...r.from);
			let [x1, y1] = px(...r.to);
			const len = Math.hypot(x1 - x0, y1 - y0) || 1;
			x1 -= ((x1 - x0) / len) * 6 * scale;
			y1 -= ((y1 - y0) / len) * 6 * scale;
			const bend = 0.12 * len;
			const cx = (x0 + x1) / 2 + ((y1 - y0) / len) * bend;
			const cy = (y0 + y1) / 2 - ((x1 - x0) / len) * bend;
			return `M${x0.toFixed(1)} ${y0.toFixed(1)}Q${cx.toFixed(1)} ${cy.toFixed(1)} ${x1.toFixed(1)} ${y1.toFixed(1)}`;
		}),
	);

	const params = new URLSearchParams();
	if (year !== undefined) params.set('year', String(year));
	if (self) params.set('place', e.id);
	const q = params.toString();

	return {
		year,
		displayWidth,
		view,
		fontSize,
		areas: areaShapes,
		hatchColors: [...new Set(areaShapes.filter((s) => s.kind === 'claimed' || s.kind === 'occupied' || s.look === 'blocks').map((s) => s.color))],
		points,
		legend,
		mapHref: `/map/${q ? `?${q}` : ''}`,
		selfOnMap: !!self && points.some((p) => p.kind === 'self'),
		routes,
	};
}
