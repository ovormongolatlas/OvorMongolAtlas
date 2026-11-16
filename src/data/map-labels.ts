/**
 * Orientation labels for the Timeline Map, drawn over the physical base map.
 *
 * These are NOT atlas entries and carry no claims of their own: they exist only
 * so readers can find their way around. Names follow period English usage
 * (postal / Wade-Giles), matching entry titles such as "North Shansi
 * Autonomous Government"; change them here if the naming table says otherwise.
 *
 * Coordinates are approximate (modern positions of the towns; rough centres of
 * the regions, which are labels only, with no borders drawn). Places that are
 * atlas entries do not belong here: they take their coordinates, with a
 * source, from the `location` field of their own entry.
 */

/** Years a name is shown for, when the name changed within the map's range. */
interface Period {
	start?: number;
	end?: number;
}

export interface ReferenceTown extends Period {
	name: string;
	lon: number;
	lat: number;
	/** Try the label on the left of the dot first, when the right side is usually crowded. */
	labelLeft?: boolean;
}

export interface AreaLabel extends Period {
	name: string;
	lon: number;
	lat: number;
	kind: 'region' | 'desert' | 'mountains' | 'water';
	/** Degrees, for labels that follow a range or a river. */
	rotate?: number;
}

export const referenceTowns: ReferenceTown[] = [
	// Names follow the map's rule for years: the name in use on 1 July.
	// Peking was renamed Peiping in June 1928, when the capital moved to Nanjing, and Peking (Beijing) again on 27 September 1949.
	{ name: 'Peking', lon: 116.4, lat: 39.9, end: 1927 },
	{ name: 'Peiping', lon: 116.4, lat: 39.9, start: 1928, end: 1949 },
	{ name: 'Peking', lon: 116.4, lat: 39.9, start: 1950 },
	{ name: 'Tientsin', lon: 117.2, lat: 39.13 },
	{ name: 'Paotow', lon: 109.84, lat: 40.66, labelLeft: true },
	{ name: 'Tatung', lon: 113.3, lat: 40.08 },
	{ name: 'Taiyuan', lon: 112.55, lat: 37.87 },
	// Urga was renamed Ulan Bator in November 1924.
	{ name: 'Urga', lon: 106.92, lat: 47.92, end: 1924 },
	{ name: 'Ulan Bator', lon: 106.92, lat: 47.92, start: 1925 },
	// Changchun was Manchukuo's capital, Hsinking, from March 1932 to August 1945.
	{ name: 'Changchun', lon: 125.32, lat: 43.88, labelLeft: true, end: 1931 },
	{ name: 'Hsinking', lon: 125.32, lat: 43.88, labelLeft: true, start: 1932, end: 1945 },
	{ name: 'Changchun', lon: 125.32, lat: 43.88, labelLeft: true, start: 1946 },
	{ name: 'Mukden', lon: 123.43, lat: 41.8 },
	{ name: 'Hailar', lon: 119.76, lat: 49.21 },
	{ name: 'Dolonnor', lon: 116.48, lat: 42.21 },
	{ name: 'Kyakhta', lon: 106.45, lat: 50.35 },
	{ name: 'Dingyuanying', lon: 105.67, lat: 38.84 },
];

/**
 * Region names are geographic and drawn small. State names come from the areas
 * in map-boundaries.ts and are drawn larger; the page keeps the two apart.
 */
export const areaLabels: AreaLabel[] = [
	{ name: 'Outer Mongolia', lon: 111.2, lat: 46.3, kind: 'region' },
	// Russia is base-map land only (no outline is drawn), so its name sits on the strip of it that shows along the top edge, north of Kyakhta.
	// Names follow the state in 1 July of each year. The Russian Empire ended in March 1917 and the Soviet Union was founded on 30 December 1922, so the first 1 July it existed on is 1923. In between, Russia was split by civil war (Far Eastern Republic around Transbaikalia 1920 to November 1922, Japanese intervention 1918 to 1922); the label there is deliberately just "Russia".
	{ name: 'Russian Empire', lon: 108.6, lat: 51.15, kind: 'region', end: 1916 },
	{ name: 'Russia', lon: 108.6, lat: 51.15, kind: 'region', start: 1917, end: 1922 },
	{ name: 'Soviet Union', lon: 108.6, lat: 51.15, kind: 'region', start: 1923 },
	{ name: 'Manchuria', lon: 125.3, lat: 46.4, kind: 'region' },
	{ name: 'Hulunbuir', lon: 120.3, lat: 48.3, kind: 'region' },
	{ name: 'Chahar', lon: 114.7, lat: 43.3, kind: 'region' },
	// Suiyuan became a special region in July 1914 (day not yet sourced; CHRONOLOGY.md, after Hirokawa 2024) and a province in 1928; before that the area was Guihua and the Ulanqab and Yekhe Juu leagues. Shown from 1915, the first 1 July it existed on.
	{ name: 'Suiyuan', lon: 108.4, lat: 42.05, kind: 'region', start: 1915 },
	{ name: 'Jehol', lon: 118.9, lat: 41.7, kind: 'region' },
	{ name: 'Ninghsia', lon: 106.9, lat: 37.3, kind: 'region' },
	// Alashan and Edsin Gol (Ejin) were Mongol banners, under Ninghsia province in the Republican period.
	{ name: 'Alashan', lon: 103.3, lat: 39.7, kind: 'region' },
	{ name: 'Edsin Gol', lon: 100.9, lat: 41.5, kind: 'region' },
	{ name: 'Kansu', lon: 99.8, lat: 38.2, kind: 'region' },
	{ name: 'Shansi', lon: 111.4, lat: 36.4, kind: 'region' },
	{ name: 'Shensi', lon: 109.0, lat: 36.6, kind: 'region' },
	// Chihli province was renamed Hopei in June 1928.
	{ name: 'Chihli', lon: 115.8, lat: 38.2, kind: 'region', end: 1927 },
	{ name: 'Hopei', lon: 115.8, lat: 38.2, kind: 'region', start: 1928 },
	{ name: 'Gobi', lon: 106.5, lat: 44.0, kind: 'desert' },
	{ name: 'Mu Us', lon: 109.0, lat: 38.45, kind: 'desert' },
	{ name: 'Yin Shan', lon: 107.9, lat: 41.15, kind: 'mountains' },
	{ name: 'Greater Khingan', lon: 121.4, lat: 46.4, kind: 'mountains', rotate: -62 },
	{ name: 'Yellow River', lon: 110.75, lat: 38.1, kind: 'water', rotate: -80 },
	{ name: 'Kherlen', lon: 114.2, lat: 47.9, kind: 'water' },
	{ name: 'Hulun Nur', lon: 118.6, lat: 49.0, kind: 'water' },
	{ name: 'Bohai', lon: 120.3, lat: 39.2, kind: 'water' },
	{ name: 'Koko Nor', lon: 100.2, lat: 36.5, kind: 'water' },
];
