/**
 * Borders drawn on the Timeline Map.
 *
 * Every border is a claim, so each one carries its own source and says, piece
 * by piece, how much it can be trusted. A border is only drawn for the years
 * in `start`–`end`.
 *
 * Precision of a sector:
 *  - 'approximate': the line shown is believed to follow the period border
 *    closely, on the stated source.
 *  - 'uncertain':   the period alignment is not known; the line is a guide only.
 *  - 'differs':     the period border is known to have run differently, but
 *    its course is not yet sourced; the line is shown so readers can see where
 *    the difference lies.
 *  - 'claim':       a line one party claimed, not a border anyone held; `cls`
 *    gives each claim its own colour.
 *  - 'internal':    an administrative boundary inside one state (e.g. Outer
 *    Mongolia within the Qing Empire); drawn in its own style with `cls`.
 *
 * Coordinates are [longitude, latitude] in decimal degrees (WGS84).
 *
 * Borders come from period maps. Outer Mongolia's frontier is Korostovets's
 * map of about 1914, checked against two later period maps (see the source
 * note); a modern compilation (AoifeIves) is used only for the Khalkhin Gol
 * claims and the 1941 demarcation there. No present-day border is used.
 * Where a border is not on any source used here, it is left undrawn and the
 * note says so.
 *
 * Years: the map shows each year as it stood on 1 July. A state founded or
 * ended in the second half of a year is therefore drawn from (or to) the next
 * (or previous) year; the panel's list of states still names every state that
 * existed at any time in the year. The one exception is a state that existed
 * only between two 1 Julys (Alashan, 1949), which is drawn for that year.
 */
import greatWall from './great-wall.json';
import outer from './outer-mongolia.json';
import period from './period-outlines.json';
import territories from './territories.json';

export type BorderPrecision = 'approximate' | 'uncertain' | 'differs' | 'claim' | 'internal';

export interface BorderSector {
	label: string;
	precision: BorderPrecision;
	note: string;
	coordinates: [number, number][];
	/** CSS class for the line, when it needs its own colour (claim lines). */
	cls?: string;
}

export interface Border {
	id: string;
	name: string;
	start: number;
	end: number;
	source: string;
	sectors: BorderSector[];
}

export const borders: Border[] = [
	{
		id: 'mongolia-russia',
		name: 'Border between Mongolia and Russia (the Soviet Union from 1922)',
		start: 1890,
		end: 1950,
		source: 'Korostovets’s Map of Mongolia (about 1914), traced from its fills for Russia (with Uriankhai) and Outer Mongolia; see “Korostovets, Map of Mongolia” under Territory outlines above. Treaty history: “Mongolia–Russia border,” Wikipedia (read October 2026).',
		sectors: [
			{
				label: 'Kyakhta line',
				precision: 'approximate',
				note: 'Set by the Treaty of Kyakhta (1727) between the Qing and Russia and confirmed in 1881. To 1911 it was the Qing–Russian border; from Mongolia’s declaration of independence in December 1911 it divided Mongolia from Russia, and from 1924 the Mongolian People’s Republic from the Soviet Union. It is reported to have stayed stable through the period, so Korostovets’s line is drawn for all of it.',
				coordinates: period.russiaMongolia as [number, number][],
			},
		],
	},
	{
		id: 'mongolia-tuva',
		name: 'Border between Mongolia and Tuva (the Soviet Union from 1944)',
		start: 1914,
		end: 1950,
		source: 'Korostovets’s Map of Mongolia (about 1914), traced from its fills for Russia (with Uriankhai) and Outer Mongolia; see “Korostovets, Map of Mongolia” under Territory outlines above. Later history: “Tuvan People’s Republic,” Wikipedia (read October 2026).',
		sectors: [
			{
				label: 'Uriankhai (Tuva) section',
				precision: 'approximate',
				note: 'Under the Qing, Tuva (Tannu Uriankhai) was part of Qing Mongolia, so no border ran here. Russia made it a protectorate in April 1914, so the line is drawn from 1914 (the Bogd Khanate also claimed it); the Tuvan People’s Republic was declared in August 1921 and joined the Soviet Union in October 1944. An agreement of July 1932 moved the line in places, giving Tuva the Dus-Dag salt mountain; that change is not on Korostovets’s map and is not drawn. Most of this section lies north of the map’s frame.',
				coordinates: period.tuvaMongolia as [number, number][],
			},
		],
	},
	{
		id: 'manchuria-russia',
		name: 'Border between Manchuria and Russia (the Soviet Union from 1922)',
		start: 1890,
		end: 1950,
		source: 'Korostovets’s Map of Mongolia (about 1914), traced from its fills for Russia (with Uriankhai) and Outer Mongolia; see “Korostovets, Map of Mongolia” under Territory outlines above. East of Blagoveshchensk: AoifeIves, “Territorial Changes along the Sino-Russian Border (1689–2023), Map 1 (of 3): Eastern Border Section.” Treaty history: “China–Russia border,” Wikipedia (read October 2026).',
		sectors: [
			{
				label: 'Argun and Amur rivers',
				precision: 'approximate',
				note: 'The Argun has been the border since the Treaty of Nerchinsk (1689) and the Amur since the Treaty of Aigun (1858); the 1911 Qiqihar Agreement shifted the Argun line slightly. On the Manchurian side it was the Qing’s border to 1911, then the Republic of China’s, and Manchukuo’s from 1932 to 1945. Korostovets’s map stops near Blagoveshchensk; from there to the edge of this map the line follows the Amur as the Treaty of Aigun line on AoifeIves’s Map 1 (Eastern Border Section), a modern compilation, traced with an affine fit to 11 towns (within about 6 km).',
				coordinates: period.russiaManchuria as [number, number][],
			},
		],
	},
	{
		id: 'outer-mongolia-qing',
		name: 'Outer Mongolia within the Qing Empire',
		start: 1890,
		end: 1911,
		source: 'The 1930s English banner map (east of 104° E) and Korostovets’s Map of Mongolia (about 1914), less Dariganga as the banner map outlines it; Dariganga’s status from Atwood, Encyclopedia of Mongolia and the Mongol Empire (2004), “Dariganga.”',
		sectors: [
			{
				label: 'Outer Mongolia under the Qing',
				precision: 'internal',
				cls: 'line-admin',
				note: 'The boundary between Outer Mongolia (the Khalkha aimags, with Khovd to the west, beyond this map) and the Inner Mongolian leagues, Hulunbuir and the Chahar lands, all within the Qing Empire. Drawn on the frontier of the 1930s banner map, which draws the Inner Mongolian banner lands whole, and on Korostovets’s line west of 104° E; this is taken to be the old administrative line, since the only land the Bogd Khanate kept beyond Qing Khalkha after the 1915 settlement was Dariganga (Atwood). Dariganga, outlined as on the same banner map, is left outside: under the Qing it was an imperial pasture under the Chahar administration at Kalgan. Check against the modern border: in Sönid Left Banner this line runs up to about 50 km south of today’s China–Mongolia border (a north-west lobe of roughly 5,000 km², about 45.1° N, 112° E, is Mongolian here and Chinese now). The drawn line on the 1930s map, traced here along the edge of the banner’s hatched lands, was checked against the source image, so the difference is probably real. The 1962 boundary treaty settled 32 disputed areas (16,329 km²) because the earlier line had never been fully fixed, and this lobe may be one of them; that is not confirmed.',
				coordinates: outer.khalkhaLine[0] as [number, number][],
			},
		],
	},

];

/**
 * State territories drawn as filled areas.
 *
 * kind:
 *  - 'ruled':   territory the government actually administered.
 *  - 'claimed': territory it claimed but did not rule.
 *  - 'context': a state that is not an atlas entry (a neighbour, or the Qing
 *    Empire before 1912), drawn lighter so the Mongol polities stand out.
 *  - 'disputed': land a period map marks as disputed between two parties.
 *  - 'occupied': land a state's troops held for a time without making it part of the state.
 *
 * `color` is the state's own colour; a state keeps it across its areas.
 *
 * `start`–`end` are the years the area is drawn for. They follow what the
 * source maps, which can be narrower than the entry's own dates.
 */
export type AreaKind = 'ruled' | 'claimed' | 'context' | 'disputed' | 'occupied';

export interface AreaSource {
	short: string;
	full: string;
	accuracy: string;
}

export interface Area {
	id: string;
	name: string;
	/** Atlas entry this area belongs to, if any. */
	entry?: string;
	kind: AreaKind;
	start: number;
	end: number;
	note: string;
	source: keyof typeof areaSources;
	coordinates: [number, number][];
	/** Further separate rings of the same area, when it is in more than one piece. */
	parts?: [number, number][][];
	/** A ring cut out of the area, e.g. the ruled part of a claim, so the two are not drawn twice. */
	exclude?: [number, number][];
	/** Where to put the area's name on the map. */
	label?: [number, number];
	/** The name as drawn on the map, if shorter than `name`; a line break is written as \n. */
	labelName?: string;
	/** The state's colour on the map and in the legend. */
	color: string;
	/** Name in the legend, when several areas share one (e.g. the MPR's yearly outlines). */
	legendName?: string;
	/** Name in the panel's list of other states, when it differs from the legend name; '' leaves the area out of that list. */
	stateName?: string;
}

/** State colours. */
const C = {
	qing: '#c9961a',
	bogd: '#e8c22e',
	occupied: '#8d8d8d',
	mpr: '#c62828',
	manchukuo: '#e07b24',
	mongol: '#00897b',
	southChahar: '#1e74c9',
	northShansi: '#8e44ad',
	disputed: '#6d6d6d',
	roc: '#7d8fa9',
	collab: '#a59a3a',
	eastHebei: '#d4a72c',
	korea: '#3949ab',
	japan: '#c2185b',
	russia: '#78909c',
	usZone: '#5c8fd6',
	dprk: '#6a1b9a',
	rok: '#1565c0',
	prc: '#e0a526',
	hulunbuir: '#4f7396',
	soviet: '#b23a3a',
	impr: '#5e35b1',
};

export const areaSources = {
	nc2014: {
		short: 'Narangoa and Cribb, Historical Atlas of Northeast Asia (2014), 1935–1940 map',
		full: 'Li Narangoa and Robert Cribb, Historical Atlas of Northeast Asia, 1590–2010: Korea, Manchuria, Mongolia, Eastern Siberia (New York: Columbia University Press, 2014), map for 1935–1940 (atlas page not yet checked), as reproduced in Dotno Dashdorj Pount, “Immigrants of Inner Mongolia: A Legacy of Pan-Mongolism, 1945–1946” (MA dissertation, 2015), Map 2, p. 19.',
		accuracy: 'Traced from a small-scale atlas map and fitted to the positions of 16 towns. Expect the lines to be off by roughly 20–40 km.',
	},
	jpMengjiang: {
		short: 'Japanese map 蒙疆地域圖 (about 1937–1939)',
		full: '蒙疆地域圖 (Map of the Mengjiang Region), Japanese, undated. Its use of 厚和 for Hohhot and its separate 察南 and 晉北 governments place it in about 1937–1939. Publisher and edition not yet identified.',
		accuracy: 'Traced from the map’s own boundary lines and fitted to 27 towns. Tested on towns left out of the fit, positions are typically within about 12 km.',
	},
	korostovets: {
		short: 'Korostovets, Map of Mongolia (about 1914)',
		full: '«Карта Монголии, составленная по данным бывшего уполномоченного в Монголии И. Я. Коростовца, при участии В. Л. Котвича» (Map of Mongolia, compiled from the data of I. Ya. Korostovets, former Russian plenipotentiary in Mongolia, with the participation of V. L. Kotvich), St Petersburg: A. Il’in cartographic establishment, about 1914, scale 80 versts to the inch; Outer Mongolia is its orange fill. The same line is on the English map “Outer Mongolia (Khalkha)” by I. J. and F. J. Korostovetz, of about 1926.',
		accuracy: 'Fitted to the map’s own latitude and longitude grid; checked on 14 towns, positions are within about 10–20 km. The English map, fitted separately to 17 towns, gives the same line. Its border with Russia is traced from the same map. Used here for the borders with Russia and Uriankhai. Used for Outer Mongolia’s outline, including its frontier with Manchuria and with Inner Mongolia west of 104° E (east of that the frontier is from the 1930s banner map, which agrees with it within about 5–10 km), because two later period maps drawn from the other side of that frontier agree with it: in the western Gobi (104.5–110.5° E) the Nakamura map of 1941 runs within about 5–15 km of it, and in the east (116–119.5° E) the Manchukuo map 滿洲國地圖 of 1 January 1934, fitted to its own grid within 2 km, runs within about 10–20 km. The line of the 1962 Sino-Mongolian treaty lies 30–60 km away in both sectors, so it was not the frontier of this period.',
	},
	nakamura1941: {
		short: 'Nakamura (1941), redrawn by Harald Krähe',
		full: 'Map of Mengjiang captioned “Source: Nakamura (1941)”, cartography by Harald Krähe: a modern redraw of a map in Nakamura Shin 中村信, 『蒙疆の経済：資源開発の現状と将来』 (Mōkyō no keizai: shigen kaihatsu no genjō to shōrai; Tokyo: Yūkosha, 1941), showing state borders, league boundaries and the Great Wall. Checked against the Japanese 蒙疆地域圖 (about 1937–1939), which draws the same southern border and Wall. The redraw is in copyright and is traced from only.',
		accuracy: 'Fitted to 24 towns; positions are typically within about 5 km.',
	},
	qingOutline: {
		short: 'Korostovets’s border with Russia; the Yalu with Korea',
		full: 'All land in this map’s frame except Russia, as Korostovets draws it (see the Korostovets entry), and Korea. Korea’s border is the Yalu River, which Korostovets’s map does not reach; it is drawn along the river (Natural Earth, public domain), the boundary the Qing and Joseon kept. Beyond the north-east edge of Korostovets’s map, Russia is completed from Natural Earth.',
		accuracy: 'The Russian border as Korostovets traces it, within about 10–20 km; the coast and the Yalu follow the physical map.',
	},
	aoife: {
		short: 'AoifeIves, “Territorial Changes along the Sino-Russian Border,” Map 2 (modern), Nomonhan inset',
		full: 'AoifeIves, “Territorial Changes along the Sino-Russian Border (1689–2023), Map 2 (of 3): Central Border Section,” a modern compilation. Used only in the Khalkhin Gol (Nomonhan) sector, for the MPR’s claim line east of the Khalkha River and the 1941 demarcation, and for Hulunbuir’s eastern edge in 1912. The map’s main frontier line (its “Russian and Mongolian reading” of the 1915 settlement) is not used: it is drawn on the course of the 1962 treaty line, which the period maps do not support. Its author notes that information on this border before 1962 is scarce and that some lines rely on modern maps.',
		accuracy: 'Traced with an affine fit to 17 towns; within about 5 km of the map as drawn.',
	},
	osaka1932: {
		short: 'Osaka Asahi Shimbun, 最新滿蒙大地圖 (February 1932)',
		full: '最新滿蒙大地圖 (Newest Large Map of Manchuria and Mongolia), specially compiled by the Osaka Asahi Shimbun, dated Showa 7 (1932), February. Used for Jehol’s boundary with Fengtian, and for the corner where Heilongjiang, Fengtian and Chahar met.',
		accuracy: 'Fitted to 12 places (coast points, lakes and railway towns) with an affine fit; residuals 3–22 km.',
	},
	banners1930: {
		short: 'Map showing the location of Mongolian banners (1930)',
		full: '蒙古盟旗記位圖 (Map showing the location of Mongolian banners), bilingual Mongolian and Chinese, dated April 1930, printed in Peiping by the Mongolian Literature Society (北平蒙文書社); about 1:6,250,000. The copy used carries a note of 10 October 1933 recording it as a gift from S. W. Boggs, Geographer of the US Department of State, and quoting the American minister to China, Nelson T. Johnson, who calls it a rough sketch by someone who had travelled in Mongolia.',
		accuracy: 'Banner lines digitised by hand and fitted to 8 towns (piecewise); residuals up to about 40 km near Ningxia. An outline of the banner, not a survey.',
	},
	bannerMap1930s: {
		short: 'English map of Mongol banners (1930s)',
		full: 'Untitled two-page map of Inner and Outer Mongolia with the Mongol banners named (Ujumuchin, Abaga, Sunit, Urat and others), English-language, from a 1930s book not yet identified (the atlas’s copy is `mapofmongols1930s.png`). Used for Outer Mongolia’s frontier with the Inner Mongolian banners from about 104° E to the Hulunbuir corner, for the outline of the Dariganga district, and for the outer boundary of the Jirim, Juu Uda and Josotu banner lands (the 1946 East Mongolian government).',
		accuracy: 'Fitted to its printed latitude–longitude grid, then corrected to seven towns on the page (residuals 4–15 km; leaving each town out, 10–26 km). The frontier runs within about 5–10 km of Korostovets’s line for most of its length.',
	},

	northChinaProvinces: {
		short: 'The provinces it governed, by its outline’s neighbours and the Yellow River',
		full: 'Drawn from the list of provinces the government nominally governed (Hebei, Shandong, Shanxi, Henan; Boyle 1972, pp. 83–91, via Wikipedia), not from a map of its territory. Outline: north, Mengjiang and Manchukuo as drawn on this map; west, the Yellow River where it divides Shanxi from Shaanxi (Natural Earth river course), then a line due south from Tongguan; east, the coast.',
		accuracy: 'As accurate as the outlines it is built from; the Shanxi–Shaanxi line follows the river. Henan’s boundary with Shaanxi south of Tongguan is drawn as a straight line.',
	},
	chinaRemainder: {
		short: 'All land not held by another state on this map',
		full: 'Not traced from a map of China. Drawn as the land in this map’s frame left over once every other state drawn for that year is taken out (Russia and Uriankhai, Korea, the Kwantung Leased Territory, Outer Mongolia, Manchukuo, the Mongol governments and Mengjiang, and the collaborator governments).',
		accuracy: 'As accurate as the neighbouring outlines it is cut from.',
	},
	koreaRivers: {
		short: 'The Yalu and Tumen rivers (Natural Earth)',
		full: 'Korea’s border with Manchuria, the Yalu and Tumen rivers, as drawn by Natural Earth (public domain physical data); it is the line the Qing and Joseon kept and that Japan and China confirmed in the Gando Convention of 1909. The line between the two Koreas from 1946 is the 38th parallel.',
		accuracy: 'Follows the rivers; the coast and islands are simplified.',
	},
	kwantung1934: {
		short: '滿洲國地圖 (Manchukuo map, 1 January 1934)',
		full: '滿洲國地圖, supplement to the 滿洲日報 (Manchuria Daily News), dated 1 January 1934 (Shōwa 9), National Archives of Singapore copy. Used for the northern boundary of the Kwantung Leased Territory.',
		accuracy: 'Fitted to 8 towns and a graticule crossing near Liaodong (affine; residuals under 4 km).',
	},

	atwood: {
		short: 'Atwood, Encyclopedia of Mongolia and the Mongol Empire (2004)',
		full: 'Christopher P. Atwood, Encyclopedia of Mongolia and the Mongol Empire (New York: Facts on File, 2004), entries “Dariganga,” “Kyakhta Trilateral Treaty,” “Sino-Mongolian War,” “Damdinsürüng, Grand Duke” and “Chahar.”',
		accuracy: 'Dates and status only. The outline drawn is the Dariganga loop on the Nakamura (1941) map, where it lies inside Korostovets’s line.',
	},
	entryOnly: {
		short: 'Position from its atlas entry',
		full: 'Placed at its seat as given in its atlas entry; no period map of its territory is used here.',
		accuracy: 'A position only, not a territory.',
	},
	combined: {
		short: 'Joined from the two maps above',
		full: 'Not traced from a map of the 1940s. Drawn by joining the 1937 Mongol territory (Narangoa and Cribb) with South Chahar and North Shansi (蒙疆地域圖), which merged with it in 1939.',
		accuracy: 'Not yet checked against a map of the 1940s.',
	},
} satisfies Record<string, AreaSource>;

const ring = (k: keyof typeof territories): [number, number][] => {
	const v = territories[k] as unknown as number[][] | number[][][];
	return (Array.isArray(v[0][0]) ? (v as number[][][])[0] : v) as [number, number][];
};
/** First ring and the further rings of an area stored as several rings. */
const T0 = (k: keyof typeof territories) => (territories[k] as unknown as [number, number][][])[0];
const TP = (k: keyof typeof territories) => (territories[k] as unknown as [number, number][][]).slice(1);

export const areas: Area[] = [
	{
		id: 'qing',
		name: 'Qing Empire',
		kind: 'context',
		start: 1890,
		end: 1911,
		note: 'All of this part of the map except Russia and Korea, including Outer Mongolia and Uriankhai (Tuva), which Russia made a protectorate only in 1914; only a thin strip of Uriankhai reaches into this map’s north-west corner. Foreign leaseholds from 1898 (Russia’s, then Japan’s, Kwantung; Britain’s Weihaiwei; Germany’s Kiaochow) stayed under nominal Qing sovereignty and are not drawn separately, nor is Russia’s occupation of Manchuria in 1900–1905. Outer Mongolia’s boundary within the empire is drawn as a line. Outer Mongolia declared independence in December 1911 and Hulunbuir early in 1912, and the last emperor abdicated on 12 February 1912, so the area is drawn through 1911.',
		source: 'qingOutline',
		coordinates: period.qing as [number, number][],
		label: [116.6, 45.4],
		color: C.qing,
	},
	{
		id: 'bogd-khanate',
		name: 'Bogd Khanate of Mongolia',
		labelName: 'Bogd Khanate\nof Mongolia',
		kind: 'context',
		start: 1912,
		end: 1919,
		note: 'Outer Mongolia declared independence on 1 December 1911 and enthroned the Bogd Khan on 29 December. The Kyakhta agreement of 1915 with Russia and China made it an autonomy under Chinese suzerainty and left its frontier to a joint commission, which never met (US State Department, International Boundary Study No. 173). The outline is Korostovets’s, with the frontier with Inner Mongolia from a 1930s English map of the banners, which draws the Inner Mongolian banner lands whole and runs within 5–10 km of Korostovets (see the source notes); China read the frontier further north, leaving Dariganga and much of the eastern Gobi in Inner Mongolia, but did not hold that line. Beyond Qing Khalkha it gained Dariganga, whose officials petitioned to join in March 1912; a Chinese force sent under Jodbajab to take it back was dispersed and he was arrested on 28 August 1912 (Atwood). Hulunbuir joined in January 1912 (drawn separately to 1915). In 1913 its troops occupied a string of places in Inner Mongolia, from Linxi, Kheshigten and the outskirts of Dolonnor to Bailingmiao and Dashetai, but withdrew after Russia ordered the campaign stopped on 28 October 1913 (Atwood; the campaign is drawn as routes). The 1915 settlement left it Dariganga but not Inner Mongolia or Hulunbuir (Atwood). It also claimed Uriankhai (Tuva) and the Altai, beyond this map. Not yet an atlas entry.',
		source: 'korostovets',
		coordinates: outer.base as [number, number][],
		label: [102.6, 46.2],
		color: C.bogd,
	},
	{
		id: 'hulunbuir-1912',
		name: 'Hulunbuir (Barga), joined to the Bogd Khanate',
		kind: 'context',
		start: 1912,
		end: 1915,
		note: 'The Barga Mongols of Hulunbuir drove out the Chinese troops and officials in the winter of 1912, proclaimed Barga independent, and joined the Bogd Khan’s government (Atwood, “Damdinsürüng”). A Russo-Chinese agreement of 1915 made Hulunbuir a special region under China, so it is joined to the Bogd Khanate to 1915 and drawn as a special region from 1916. Outline: west, the Outer Mongolian line (Korostovets); east, the Bogd Khanate’s claim line along the Khingan on the AoifeIves map; south, a straight join to the corner where Heilongjiang met Chahar on the Osaka Asahi map of 1932. The southern edge is the least certain part.',
		source: 'aoife',
		coordinates: outer.barga1912 as [number, number][],
		stateName: 'Bogd Khanate of Mongolia',
		color: C.bogd,
		legendName: 'Bogd Khanate of Mongolia',
	},
	{
		id: 'hulunbuir-special-region',
		name: 'Hulunbuir Special Region',
		labelName: 'Hulunbuir\nSpecial Region',
		kind: 'context',
		start: 1916,
		end: 1919,
		note: 'Under the 1915 Russo-Chinese agreement on Hulunbuir, signed after the Kyakhta treaty, Hulunbuir became a special district directly under the government of China. On 28 January 1920, after a telegram from Barga representatives in Qiqihar, the government issued a decree ending its status as a “special territory” (B. D. Tsybenov, L. V. Kuras and V. E. Tsyrempilova, “Institutions of Public Government in Manchu-Mongolian Polities, 1900s–1920s: A Case Study of Hulunbuir,” Oriental Studies 16, no. 4 (2023): 718–726). It is therefore drawn for 1916–1919 and as plain China from 1920; the Kaiseikan atlas of March 1920 colours it as part of Heilongjiang. The agreement is dated 24 October 1915 by Tsybenov and his co-authors and 6 November 1915 by Wikipedia (“Hulunbuir,” read October 2026); the thirteen days are the gap between the Julian and Gregorian calendars, so these are probably the same date. Wikipedia adds that Russia kept partial control. Same outline as 1912–1915, with the same uncertain southern edge.',
		source: 'aoife',
		coordinates: outer.barga1912 as [number, number][],
		label: [119.7, 49.4],
		stateName: '',
		color: C.hulunbuir,
		legendName: 'Hulunbuir Special Region (under China)',
	},
	{
		id: 'bogd-1913',
		name: 'Shilingol and Ulaanchab, ground of the Bogd Khanate’s 1913 campaign',
		entry: 'five-roads-campaign',
		kind: 'occupied',
		start: 1913,
		end: 1913,
		note: 'The ground of the Bogd Khanate’s 1913 campaign, not land annexed to it. On 23 January 1913 Urga ordered the neighbouring leagues of Shilingol and Ulaanchab to mobilise 2,000 troops, and the campaign’s base camps lay on their open steppe; in summer 1913 its troops advanced from there and at their furthest occupied Linxi, Kheshigten Banner and Jingpeng, the outskirts of Dolonnor, Pangjiang, Erfenzi, Batu-Khaalga (Bailingmiao), Dashetai and Ulaan Oboo (Atwood, “Sino-Mongolian War”). The leagues themselves did not join the Bogd Khanate: Jagchid writes that Ulanchab’s nobles, though “comparatively pro-Ulaanbaatar,” only expressed sympathy under pressure from Beijing, and that after Outer Mongolian troops arrested Shilingol’s league head Yangsang, the only one who opposed independence, his deputy kept a “wait-and-see” policy (The Last Mongol Prince, pp. 13–14). Russia ordered the campaign stopped on 28 October 1913 and the troops withdrew, a withdrawal the 1915 Kyakhta agreement formalised (Atwood); Jagchid has the force sent against Dolonnor withdrawing under Chinese military pressure (p. 15). The area is drawn for 1913 as a whole, since no source gives the front on 1 July; places occupied outside it are marked as rings. Pangjiang is placed from a 2017 report, which disagrees with Jagchid on its bearing from the Sünid Right prince’s residence (see its marker). The leagues are outlined as on the Nakamura (1941) map, with Shilingol’s ten banners and Ulaanchab’s six, without the Chinese-settled counties around Hohhot and Baotou, which were under Suiyuan. The Hetao plain, the irrigated farmland of the Wuyuan and Linhe counties along the Yellow River, is also left out: the bases were on the open steppe, and none of the county seats is among the places occupied. Its edge is approximated as the land within 45 km of the river, up to the foot of the Lang Shan. Checked against the 1930s English banner map, whose Shilingol and Ulaanchab banners (Üjümchin to Urad) fall inside the outline, with Juu Uda and the Chahar banners outside it.',
		source: 'nakamura1941',
		coordinates: ring('bogd1913'),
		label: [112.6, 43.6],
		labelName: 'Bogd Khanate’s\ncampaign (1913)',
		color: C.bogd,
		legendName: 'Ground of the Bogd Khanate’s campaign',
	},

	{
		id: 'outer-mongolia-1920',
		name: 'Outer Mongolia, occupied by China',
		labelName: 'Outer Mongolia,\noccupied by China',
		kind: 'context',
		start: 1920,
		end: 1920,
		note: 'Xu Shuzheng’s troops entered Urga in October 1919 and China ended Outer Mongolia’s autonomy that autumn; Wikipedia’s articles put the formal steps between 28 October and 17 November 1919. China held it until Ungern-Sternberg’s troops took Urga early in 1921. Drawn on Outer Mongolia’s Qing line, without Dariganga, which China counted as part of the Chahar Special Region from 1914 (Chinese Wikipedia, “達里岡厓牧場,” read October 2026) and which a Japanese map drawn during the occupation puts on the Inner Mongolian side: “Manchuria and Eastern Inner Mongolia” (満洲及東部内蒙古), in Kaiseikan’s Standard Atlas of Japan (Tokyo, March 1920), which also draws Outer Mongolia’s edge as the boundary of the Inner Mongolian princes’ lands rather than as a national border. Mongolian sources say it was governed from Urga throughout, and no source used here says how China ran it in 1920; with all of Outer Mongolia under Chinese control that year, the difference is one of administration, drawn here as China’s own arrangement.',
		source: 'korostovets',
		coordinates: outer.khalkha as [number, number][],
		label: [102.6, 46.2],
		stateName: '',
		color: C.occupied,
	},
	{
		id: 'bogd-khanate-1921',
		name: 'Bogd Khanate of Mongolia (restored)',
		labelName: 'Bogd Khanate\nof Mongolia',
		kind: 'context',
		start: 1921,
		end: 1921,
		note: 'Restored when Ungern-Sternberg’s troops took Urga early in 1921; on 1 July 1921 Urga was still held by the restored government. The Mongolian People’s Party and Soviet troops entered Urga that July, and the Bogd Khan stayed on as a limited monarch under a people’s government until his death in May 1924. Same outline as before, except Dariganga, drawn with China: after Ungern’s seizure of Urga, China again sent Jodbajab to take Dariganga, and he held it until a Soviet Kalmyk force with Mongolian partisans drove him out in August 1921 (Atwood).',
		source: 'korostovets',
		coordinates: outer.khalkha as [number, number][],
		label: [102.6, 46.2],
		color: C.bogd,
		legendName: 'Bogd Khanate of Mongolia',
	},	{
		id: 'bogd-khanate-1922',
		name: 'Bogd Khanate of Mongolia (restored)',
		labelName: 'Bogd Khanate\nof Mongolia',
		kind: 'context',
		start: 1922,
		end: 1923,
		note: 'The Bogd Khan reigned as a limited monarch under the people’s government that Soviet and Mongolian revolutionary troops installed in July 1921, until his death in May 1924. Dariganga, retaken from Jodbajab’s Chinese troops in August 1921, is part of it again from 1922 (Atwood).',
		source: 'korostovets',
		coordinates: outer.base as [number, number][],
		label: [102.6, 46.2],
		color: C.bogd,
		legendName: 'Bogd Khanate of Mongolia',
	},

	{
		id: 'mpr-1924',
		name: 'Mongolian People’s Republic',
		labelName: 'Mongolian\nPeople’s Republic',
		kind: 'context',
		start: 1924,
		end: 1934,
		note: 'Proclaimed on 26 November 1924, after the Bogd Khan died in May. No successor was enthroned, so 1924 is drawn as the MPR. Same outline as the Bogd Khanate. Near the Khalkha River, Korostovets’s line runs close to the river itself, the line Manchukuo later claimed, and the 1934 Manchukuo map draws the same; the MPR’s claim further east is drawn once it was fought over, from 1935. Not yet an atlas entry. In the Üjümüchin sector of Shilingol the frontier is Nakamura’s line (1941), which agrees within about 10–30 km with Atwood’s map of the Qing leagues and the 1962 treaty line; the 1930s banner map, used elsewhere, puts it 30–80 km further south, which would give northern Üjümüchin to Mongolia, and no source has those banners joining the Bogd Khanate or the MPR.',
		source: 'korostovets',
		coordinates: outer.base as [number, number][],
		label: [102.6, 46.2],
		color: C.mpr,
	},
	{
		id: 'mpr-1935',
		name: 'Mongolian People’s Republic',
		labelName: 'Mongolian\nPeople’s Republic',
		kind: 'context',
		start: 1935,
		end: 1941,
		note: 'From 1935 Manchukuo and the MPR fought over the strip between the Khalkha River and the line the MPR claimed east of it; the first clashes came early in 1935, and the battles of Khalkhin Gol were fought there in 1939. That strip is drawn as disputed, and the MPR keeps Korostovets’s line, close to the river. The dispute ended only with the demarcation documents signed on 15 October 1941 (International Boundary Study No. 173), so it runs to 1941.',
		source: 'korostovets',
		coordinates: outer.base as [number, number][],
		label: [102.6, 46.2],
		color: C.mpr,
	},
	{
		id: 'mpr-1942',
		name: 'Mongolian People’s Republic',
		labelName: 'Mongolian\nPeople’s Republic',
		kind: 'context',
		start: 1942,
		end: 1950,
		note: 'Demarcation in the Nomonhan region began in September 1940, and the documents were signed by Manchukuo and Outer Mongolia on 15 October 1941 (International Boundary Study No. 173); along the frontier with Manchukuo the line shown is that demarcation, which followed the MPR’s claim for most of its length (AoifeIves inset), so the MPR now takes most of the Khalkhin Gol strip and Buir Nuur. The Republic of China recognised Mongolia’s independence within its existing borders in January 1946; the rest of the line is Korostovets’s, unchanged from before.',
		source: 'aoife',
		coordinates: outer.mpr1942 as [number, number][],
		label: [102.6, 46.2],
		color: C.mpr,
	},
	{
		id: 'nomonhan-disputed',
		name: 'Khalkhin Gol frontier, disputed by the MPR and Manchukuo',
		kind: 'disputed',
		start: 1935,
		end: 1941,
		note: 'The strip between the Khalkha River, which Manchukuo claimed as the border, and the line east of it that the MPR claimed. It is drawn as disputed from 1935, when the first clashes took place, to 1941: the battles of Khalkhin Gol were fought here in 1939, a truce followed in the autumn, demarcation began in September 1940, and the documents were signed on 15 October 1941 (International Boundary Study No. 173). The strip runs from Buir Nuur south-east, between Korostovets’s line, close to the river, and the MPR’s claim line from the magnified Nomonhan inset of the AoifeIves map.',
		source: 'aoife',
		coordinates: outer.nomonhan[0] as [number, number][],
		parts: outer.nomonhan.slice(1) as [number, number][][],
		label: [118.25, 47.9],
		labelName: 'Khalkhin Gol\n(disputed)',
		color: C.disputed,
		legendName: 'Disputed: Khalkhin Gol strip (MPR and Manchukuo)',
	},
	{
		id: 'manchukuo-1932',
		name: 'Manchukuo',
		kind: 'context',
		start: 1932,
		end: 1932,
		note: 'Founded on 1 March 1932. On 1 July 1932 it did not yet hold Jehol, which it claimed and took early in 1933; Jehol is drawn hatched as its claim. Jehol’s boundary with Fengtian is traced from the Osaka Asahi Shimbun’s map of February 1932; the rest of the outline is as for 1933. The hatched area also takes in some Chahar land west of Jehol that Manchukuo held later, as the two maps disagree there.',
		source: 'nc2014',
		coordinates: ring('manchukuo1932'),
		label: [123.3, 44.6],
		color: C.manchukuo,
	},
	{
		id: 'jehol-1932',
		name: 'Jehol, claimed by Manchukuo',
		kind: 'claimed',
		start: 1932,
		end: 1932,
		note: 'Manchukuo counted Jehol as its own from its founding but took it only in the campaign of February–March 1933, so in mid-1932 it was a claim. Jehol’s eastern boundary is from the Osaka Asahi Shimbun’s 最新滿蒙大地圖 (February 1932).',
		source: 'osaka1932',
		coordinates: ring('jehol1932'),
		color: C.manchukuo,
		legendName: 'Claimed by Manchukuo',
	},
	{
		id: 'manchukuo-1933',
		name: 'Manchukuo',
		kind: 'context',
		start: 1933,
		end: 1934,
		note: 'Drawn as Narangoa and Cribb map it for 1935–1940, including Jehol (taken early in 1933), and carried out to the period lines around it: Korostovets’s border with Russia, the Outer Mongolian line, the Yalu, the coast (leaving out Japan’s Kwantung Leased Territory, whose boundary is traced from the 1934 Manchukuo map), and the Great Wall south of Jehol (the 1933 Tanggu truce line), so that no unassigned strip is left between them. Thin strips between it and the Mongol territories are split down the middle. Before the fighting of 1935 its border with the MPR is Korostovets’s line near the Khalkha River, which the 1934 Manchukuo map also draws. Smaller changes within 1933–1945 are not shown. In eastern Shilingol it follows the period maps that agree: its frontier with Outer Mongolia in the Üjümüchin banners is Nakamura’s line (1941), within about 10–30 km of Atwood’s map of the Qing leagues and of the 1962 treaty line, about 30–80 km north of the 1930s banner map used elsewhere; and the whole Shilingol League, out to its boundary with Juu Uda, is outside Manchukuo, as Nakamura and both of Atwood’s maps draw it (Narangoa and Cribb’s atlas puts a band of about 29,000 km² there in Manchukuo).',
		source: 'nc2014',
		coordinates: ring('manchukuo1933'),
		label: [121.6, 43.7],
		color: C.manchukuo,
	},
	{
		id: 'manchukuo',
		name: 'Manchukuo',
		kind: 'context',
		start: 1935,
		end: 1941,
		note: 'Drawn as Narangoa and Cribb map it for 1935–1940, including Jehol (taken early in 1933), and carried out to the period lines around it: Korostovets’s border with Russia, the Outer Mongolian line, the Yalu, the coast (leaving out Japan’s Kwantung Leased Territory, whose boundary is traced from the 1934 Manchukuo map), and the Great Wall south of Jehol (the 1933 Tanggu truce line), so that no unassigned strip is left between them. Thin strips between it and the Mongol territories are split down the middle. Its border with the MPR stops at the disputed Khalkhin Gol strip. Smaller changes within 1933–1945 are not shown. In eastern Shilingol it follows the period maps that agree: its frontier with Outer Mongolia in the Üjümüchin banners is Nakamura’s line (1941), within about 10–30 km of Atwood’s map of the Qing leagues and of the 1962 treaty line, about 30–80 km north of the 1930s banner map used elsewhere; and the whole Shilingol League, out to its boundary with Juu Uda, is outside Manchukuo, as Nakamura and both of Atwood’s maps draw it (Narangoa and Cribb’s atlas puts a band of about 29,000 km² there in Manchukuo).',
		source: 'nc2014',
		coordinates: ring('manchukuo'),
		label: [121.6, 43.7],
		color: C.manchukuo,
	},
	{
		id: 'manchukuo-1942',
		name: 'Manchukuo',
		kind: 'context',
		start: 1942,
		end: 1945,
		note: 'As for 1940–1941, with its western border on the line demarcated with the MPR in 1941.',
		source: 'nc2014',
		coordinates: ring('manchukuo1942'),
		label: [121.6, 43.7],
		color: C.manchukuo,
	},
	{
		id: 'dariganga-chahar-1914',
		entry: 'dariganga',
		name: 'Dariganga, assigned to Chahar by China',
		labelName: 'Dariganga\n(Chahar on paper)',
		kind: 'claimed',
		start: 1914,
		end: 1919,
		note: 'China counted Dariganga as part of the Chahar Special Region from its creation in 1914 (Chinese Wikipedia, “達里岡厓牧場,” read October 2026), and the US State Department’s International Boundary Study No. 173 counts it part of Chinese Inner Mongolia through 1924. In practice it was governed from Urga: its officials had petitioned to join Mongolia in March 1912, and Chinese troops held it only for some months of 1921 (Atwood), so it is hatched in China’s colour as an assignment on paper, over the Mongolian state that ran it. For 1920–1921, when China held it, it is drawn with China. Outline: Dariganga as the 1930s English banner map draws it.',
		source: 'bannerMap1930s',
		coordinates: outer.dariganga1930s as [number, number][],
		label: [113.6, 45.6],
		stateName: '',
		color: C.roc,
		legendName: 'Assigned to Chahar by China, not administered',
	},
	{
		id: 'dariganga-chahar-1922',
		entry: 'dariganga',
		name: 'Dariganga, assigned to Chahar by China',
		labelName: 'Dariganga\n(Chahar on paper)',
		kind: 'claimed',
		start: 1922,
		end: 1924,
		note: 'China counted Dariganga as part of the Chahar Special Region from its creation in 1914 (Chinese Wikipedia, “達里岡厓牧場,” read October 2026), and the US State Department’s International Boundary Study No. 173 counts it part of Chinese Inner Mongolia through 1924. In practice it was governed from Urga: its officials had petitioned to join Mongolia in March 1912, and Chinese troops held it only for some months of 1921 (Atwood), so it is hatched in China’s colour as an assignment on paper, over the Mongolian state that ran it. For 1920–1921, when China held it, it is drawn with China. Outline: Dariganga as the 1930s English banner map draws it.',
		source: 'bannerMap1930s',
		coordinates: outer.dariganga1930s as [number, number][],
		label: [113.6, 45.6],
		stateName: '',
		color: C.roc,
		legendName: 'Assigned to Chahar by China, not administered',
	},
	{
		id: 'dariganga-disputed',
		entry: 'dariganga',
		name: 'Dariganga, held by the MPR and claimed by Mengjiang',
		kind: 'disputed',
		start: 1936,
		end: 1945,
		note: 'Drawn as disputed from 1936, when the Mongolian Military Government was founded (May 1936), to 1945. Japanese maps of 1937–1941 (蒙疆地域圖; Nakamura) draw Dariganga inside Mengjiang, and a modern map of the border’s history (AoifeIves, “Territorial Changes along the Sino-Russian Border,” map 2) draws the Military Government’s claim of May 1936 round it; the MPR held it throughout. Under the Qing it was the emperor’s herding district, answering to the eight Chahar banners on the Inner Mongolian side. Its officials petitioned to join Mongolia in March 1912 (Atwood; Mongoltoli has its chief submitting in 1911), and it stayed under Mongolian administration from then on, except in 1921, when Chinese troops held it for some months (drawn for 1921): a banner of Khan Khentii Uul aimag from 1925, of Dornod from 1931, and of Javkhlant Sharga (Sükhbaatar) from 1942 (Mongoltoli, “Дарьганга уулын хошуу”). Earlier disagreements: the Republic of China assigned it to the Chahar Special Region in 1914, drawn hatched for 1914–1919 and 1922–1924; the Republic tried to bring Dariganga’s herds under its own jurisdiction (Mongoltoli); the US State Department’s International Boundary Study No. 173 counts it part of Chinese Inner Mongolia through 1924; and the same modern map draws the Chinese reading of the 1915 Kyakhta settlement as leaving it outside autonomous Mongolia. Outline: the loop that the Nakamura (1941) map draws round it, where it lies inside the Outer Mongolian line.',
		source: 'nakamura1941',
		coordinates: outer.dariganga as [number, number][],
		label: [113.6, 45.6],
		labelName: 'Dariganga\n(disputed)',
		color: C.disputed,
		legendName: 'Disputed: Dariganga (MPR and Mengjiang)',
	},
	{
		id: 'mlaag-claimed',
		name: 'Claimed by the Mongolian Allied League Autonomous Government',
		entry: 'mongolian-allied-league-autonomous-government',
		kind: 'claimed',
		start: 1938,
		end: 1939,
		note: 'Territory the government claimed but did not rule, including the Ordos (Yeke Juu League). Drawn as the atlas maps it for 1937. Mengjiang’s own images of itself in these years include the Ordos: a Japanese pictorial map of the region, which shows South Chahar and North Shansi as separate governments (so 1937–1939), draws Yeke Juu League (伊克昭盟) inside the state, with the Great Wall as its southern edge; and a commemorative watch fob dated 1938 (成紀七三三年, 民國二十七年) for the tour of Japan and Manchukuo by the county and banner heads of the three Mengjiang governments (蒙疆三自治政府縣旗長日滿視察紀念), is cut to an outline of Mengjiang whose crenellated southern edge, the Great Wall, takes in the Ordos. Both are known to the atlas from photographs only; they show the claim, not what the government held.',
		source: 'nc2014',
		coordinates: ring('mlaagClaimed'),
		exclude: ring('mlaagRuled'),
		color: C.mongol,
		legendName: 'Claimed by the Mongolian Allied League government',
	},
	{
		id: 'mlaag-ruled',
		name: 'Mongolian Allied League Autonomous Government',
		entry: 'mongolian-allied-league-autonomous-government',
		kind: 'ruled',
		start: 1938,
		end: 1939,
		note: 'Territory it ruled: the 1936 area of the Mongolian Military Government plus what Japanese and Mongol forces took in Operation Chahar, chiefly Hohhot and Baotou in mid-October 1937 (14 and 17 October in the Wikipedia and WW2DB chronologies; one account dates Hohhot’s fall to 27 October). A Mongolian Congress at Hohhot founded the government on 27 October 1937 and it was formally inaugurated on 1 December (see its entry), so it is drawn from 1938, its first mid-year. West of Baotou it stops short of the Hetao plain, which stayed in Chinese hands. Its northern edge is drawn up to the Outer Mongolian line, and narrow strips left between this area, South Chahar, North Shansi and Manchukuo are tracing error, not unclaimed land, and are drawn as part of it.',
		source: 'nc2014',
		coordinates: ring('mlaagRuled'),
		label: [114.0, 42.55],
		labelName: 'Mongolian Allied League\nAutonomous Government',
		color: C.mongol,
		legendName: 'Mongolian Allied League Autonomous Government',
	},
	{
		id: 'scag',
		name: 'South Chahar Autonomous Government',
		entry: 'south-chahar-autonomous-government',
		kind: 'ruled',
		start: 1938,
		end: 1939,
		note: 'Established at Kalgan on 4 September 1937 (see its entry), so it is drawn from 1938, its first mid-year. Drawn from the Japanese map’s outline of 察南政府, around Kalgan and Xuanhua.',
		source: 'jpMengjiang',
		coordinates: ring('scag'),
		label: [114.94, 40.32],
		labelName: 'South\nChahar',
		color: C.southChahar,
	},
	{
		id: 'nsag',
		name: 'North Shansi Autonomous Government',
		entry: 'north-shansi-autonomous-government',
		kind: 'ruled',
		start: 1938,
		end: 1939,
		note: 'Established at Datong on 15 October 1937 (see its entry), so it is drawn from 1938, its first mid-year. Drawn from the Japanese map’s outline of 晉北政府, around Datong.',
		source: 'jpMengjiang',
		coordinates: ring('nsag'),
		label: [112.72, 39.66],
		labelName: 'North\nShansi',
		color: C.northShansi,
	},
	{
		id: 'mmg-1936',
		name: 'Mongolian Military Government',
		entry: 'mongolian-military-government',
		kind: 'ruled',
		start: 1936,
		end: 1936,
		note: 'Prince De’s Mongolian Military Government as Narangoa and Cribb map it for 1936. Founded in May 1936, so 1936 is its first mid-year. Its northern edge is drawn up to the Outer Mongolian line, which Japanese maps of the time accept except at Dariganga.',
		source: 'nc2014',
		coordinates: ring('mmg1936'),
		label: [114.05, 42.75],
		labelName: 'Mongolian\nMilitary Government',
		color: C.mongol,
	},
	{
		id: 'mmg-1937',
		name: 'Mongolian Military Government',
		entry: 'mongolian-military-government',
		kind: 'ruled',
		start: 1937,
		end: 1937,
		note: 'Fu Zuoyi’s forces took Bailingmiao by dawn on 24 November 1936 (Jagchid, as cited in the Bailingmiao entry; the WW2DB chronology gives the same date) and pushed the Military Government out of the western part of its 1936 area. For 1937 that part is left out, along the dotted line with which Narangoa and Cribb mark the approximate area of the Suiyuan Mongol Local Autonomous Political Council, the body Fu Zuoyi sponsored there. The government lasted until its successor was founded in October 1937.',
		source: 'nc2014',
		coordinates: ring('mmg1937'),
		label: [114.4, 42.75],
		labelName: 'Mongolian\nMilitary Government',
		color: C.mongol,
	},
	{
		id: 'mengjiang-1940',
		name: 'Mengjiang',
		entry: 'mengjiang',
		kind: 'ruled',
		start: 1940,
		end: 1945,
		note: 'The merged government (from 1939 the Mongolian Allied Autonomous Government, from 1941 the Mongolian Autonomous State). The three governments merged on 1 September 1939, so it is drawn from 1940, and 1939 shows the three parts. The Hetao plain is left out: Japanese troops took Wuyuan and Linhe in early February 1940 but had lost Wuyuan again by 1 April, and the area stayed in Chinese hands (Wikipedia and WW2DB battle chronologies). In eastern Shilingol it follows the period maps that agree: its frontier with Outer Mongolia in the Üjümüchin banners is Nakamura’s line (1941), within about 10–30 km of Atwood’s map of the Qing leagues and of the 1962 treaty line, about 30–80 km north of the 1930s banner map used elsewhere; and the whole Shilingol League, out to its boundary with Juu Uda, is outside Manchukuo, as Nakamura and both of Atwood’s maps draw it (Narangoa and Cribb’s atlas puts a band of about 29,000 km² there in Manchukuo).',
		source: 'combined',
		coordinates: ring('mengjiang1939'),
		label: [113.04, 41.96],
		color: C.mongol,
	},
	{
		id: 'mengjiang-claimed-1940',
		name: 'Claimed by Mengjiang',
		entry: 'mengjiang',
		kind: 'claimed',
		start: 1940,
		end: 1945,
		note: 'The part of the 1937 claim that Mengjiang did not rule, chiefly the Ordos (Yekejuu League). The Nakamura map of 1941 draws Mengjiang’s state border round the whole Ordos, south to the Great Wall and west to the Yellow River, and the Japanese 蒙疆地域圖 does the same; this is the area drawn here, from Narangoa and Cribb’s 1937 claim. It is a claim: in spring 1938 Altanochir of Hanggin Banner asked Demchugdongrub for troops to break free of Fu Zuoyi (Wikipedia, “Altanochir”), and the Nationalist Suiyuan government kept offices in the Ordos through the war (Chinese Wikipedia, “伊克昭盟”). No source used here names an Ordos banner that Mengjiang ruled.',
		source: 'nakamura1941',
		coordinates: ring('mengjiangClaimed1940'),
		color: C.mongol,
		legendName: 'Claimed by Mengjiang',
	},
	{
		id: 'alashan-1949',
		name: 'Mongolian Autonomous Government (Alashan)',
		entry: 'mongolian-autonomous-government-alashan',
		kind: 'ruled',
		start: 1949,
		end: 1949,
		note: 'Proclaimed at Dingyuanying (Bayanhot) on 10 August 1949; Demchugdongrub left on 20 September, and the leaders who stayed surrendered on 5 October (see its entry). It is drawn for 1949 although it did not yet exist on 1 July, since it existed only that summer and autumn. The area drawn is Alashan Banner, where it sat and whose prince, Damzana, was its vice-chairman, as the banner map of 1930 outlines it, closed up to the Outer Mongolian line that the banner bordered. Between about Dengkou and Shizuishan that map makes the Yellow River the banner’s eastern edge; since the sketch map puts the river up to about 60 km too far west there, that stretch is drawn on the river itself. How far the government’s writ actually ran is not mapped in any source used here.',
		source: 'banners1930',
		coordinates: ring('alashan'),
		label: [103.5, 40.9],
		labelName: 'Mongolian Autonomous\nGovernment',
		color: C.mongol,
	},
	{
		id: 'council-1934',
		name: 'Mongolian Political Affairs Council',
		entry: 'mongolian-political-affairs-council',
		labelName: 'Mongolian Political\nAffairs Council',
		kind: 'ruled',
		start: 1934,
		end: 1934,
		note: 'The jurisdiction of the Mongolian Political Affairs Council, set up at Bat-khaalag (Bailingmiao) on 23 April 1934 under the Nanjing government’s sanction, with Yondonwangchug as nominal chairman and De Wang holding real authority (Jagchid; Zorigt, “Self-Rule Movement”). Zorigt gives its jurisdiction as ten Shilingol banners, six Ulanchab banners, twelve Chahar banners and seven Yekejuu banners. It ran the banners’ affairs inside China: the leagues stayed formally within the provinces of Chahar and Suiyuan, and the Chinese counties among them answered to the provinces. Nanjing ordered it dissolved in May 1936, when the Japanese-backed Mongolian Military Government superseded it. No map of its area has been found, so it is drawn as the four leagues on the Nakamura (1941) map, which overstates it in two places: the 1941 Chahar league took in Chinese counties such as Zhangbei and Dehua, among whose lands the twelve Chahar banners lay in 1934, and the Yikezhao outline is all of the Ordos inside the Great Wall and the Yellow River, Chinese-settled county land included. As on the 1913 map, the counties around Hohhot and Baotou and the Hetao plain are left out, and the strip up to the Outer Mongolian line is closed onto the leagues.',
		source: 'nakamura1941',
		coordinates: ring('council1934'),
		label: [112.4, 42.6],
		color: C.mongol,
		legendName: 'Mongolian Political Affairs Council (banner affairs, within China)',
	},
	{
		id: 'council-1935',
		name: 'Mongolian Political Affairs Council',
		entry: 'mongolian-political-affairs-council',
		labelName: 'Mongolian Political\nAffairs Council',
		kind: 'ruled',
		start: 1935,
		end: 1935,
		note: 'The jurisdiction of the Mongolian Political Affairs Council, set up at Bat-khaalag (Bailingmiao) on 23 April 1934 under the Nanjing government’s sanction, with Yondonwangchug as nominal chairman and De Wang holding real authority (Jagchid; Zorigt, “Self-Rule Movement”). Zorigt gives its jurisdiction as ten Shilingol banners, six Ulanchab banners, twelve Chahar banners and seven Yekejuu banners. It ran the banners’ affairs inside China: the leagues stayed formally within the provinces of Chahar and Suiyuan, and the Chinese counties among them answered to the provinces. Nanjing ordered it dissolved in May 1936, when the Japanese-backed Mongolian Military Government superseded it. No map of its area has been found, so it is drawn as the four leagues on the Nakamura (1941) map, which overstates it in two places: the 1941 Chahar league took in Chinese counties such as Zhangbei and Dehua, among whose lands the twelve Chahar banners lay in 1934, and the Yikezhao outline is all of the Ordos inside the Great Wall and the Yellow River, Chinese-settled county land included. As on the 1913 map, the counties around Hohhot and Baotou and the Hetao plain are left out, and the strip up to the Outer Mongolian line is closed onto the leagues.',
		source: 'nakamura1941',
		coordinates: ring('council1935'),
		label: [112.4, 42.6],
		color: C.mongol,
		legendName: 'Mongolian Political Affairs Council (banner affairs, within China)',
	},


	{
		id: 'roc-1912',
		name: 'Republic of China',
		kind: 'context',
		start: 1912,
		end: 1912,
		note: 'The Republic of China was proclaimed on 1 January 1912 and the last Qing emperor abdicated on 12 February 1912. Drawn as the land in this part of the map that no other state held. Its provinces are not all drawn yet; the provincial lines shown are those sourced so far. Not yet an atlas entry.',
		source: 'chinaRemainder',
		coordinates: ring('roc1912'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},	{
		id: 'roc-1913',
		name: 'Republic of China',
		kind: 'context',
		start: 1913,
		end: 1913,
		note: 'Without the Shilingol and Ulaanchab leagues, held for the Bogd Khanate in 1913 (see that area’s note); they are drawn back in China from 1914.',
		source: 'chinaRemainder',
		coordinates: ring('roc1913'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},	{
		id: 'roc-1914',
		name: 'Republic of China',
		kind: 'context',
		start: 1914,
		end: 1915,
		note: 'As for 1912: the Mongolian troops withdrew from Inner Mongolia after Russia ordered the campaign stopped on 28 October 1913, and the Kyakhta agreement of 1915 confirmed the withdrawal (Atwood). Hulunbuir stays with the Bogd Khanate to 1915.',
		source: 'chinaRemainder',
		coordinates: ring('roc1912'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},
	{
		id: 'roc-1916',
		name: 'Republic of China',
		kind: 'context',
		start: 1916,
		end: 1919,
		note: 'Hulunbuir, a special region under the central government from 1915 to January 1920, is drawn separately. Two attempts to restore a monarchy fall in these years and are not drawn, since neither changed the borders. Yuan Shikai, president since 1912, accepted the throne on 12 December 1915 and proclaimed the Empire of China with the reign name Hongxian from 1 January 1916; facing revolt in the southern provinces, he abandoned it on 22 March 1916 and died on 6 June 1916, so on 1 July 1916 the Republic stood again (Wikipedia, “Empire of China (1915–1916),” read October 2026). From 1 to 12 July 1917 the general Zhang Xun restored the last Qing emperor, Puyi, in Beijing (Wikipedia, “Manchu Restoration,” read October 2026). That span includes this map’s date for 1917, but the restoration was put down within twelve days and did not change the borders, so 1917 is still drawn as the Republic. Jagchid writes that the Mongol nobles in Beijing, except Gungsangnorbu, openly supported the restoration, as did the Shilingol leaders, and that Nayantu, the Khalkha prince, led the Mongol nobles who backed Yuan’s throne (The Last Mongol Prince, p. 16). Warlord rule (the Beiyang period) and the Northern Expedition of 1926–1928 are not drawn: the map shows the internationally recognised state.',
		source: 'chinaRemainder',
		coordinates: ring('roc1912'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},	{
		id: 'roc-1920',
		name: 'Republic of China',
		kind: 'context',
		start: 1920,
		end: 1921,
		note: 'With Hulunbuir, whose special status ended on 28 January 1920, and with Dariganga, which China counted as part of the Chahar Special Region (see Outer Mongolia’s 1920 note). In 1920 China also held Outer Mongolia, drawn separately in grey. In 1921, after Ungern’s seizure of Urga, China sent the Chahar official Jodbajab to take Dariganga, and he held it until a Soviet Kalmyk force with Mongolian partisans drove him out in August 1921 (Atwood, “Dariganga”), so on 1 July 1921 it is still drawn with China.',
		source: 'chinaRemainder',
		coordinates: ring('roc1920'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},	{
		id: 'roc-1922',
		name: 'Republic of China',
		kind: 'context',
		start: 1922,
		end: 1931,
		note: 'Including Hulunbuir, as from 1920; Dariganga is with Mongolia again from August 1921. Warlord rule (the Beiyang period) and the Northern Expedition of 1926–1928 are not drawn: the map shows the internationally recognised state.',
		source: 'chinaRemainder',
		coordinates: ring('roc1916'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},
	{
		id: 'roc-1932',
		name: 'Republic of China',
		kind: 'context',
		start: 1932,
		end: 1932,
		note: 'Without Manchukuo, founded on 1 March 1932. Jehol, still held by China but claimed by Manchukuo, is drawn hatched.',
		source: 'chinaRemainder',
		coordinates: ring('roc1932'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},
	{
		id: 'roc-1933',
		name: 'Republic of China',
		kind: 'context',
		start: 1933,
		end: 1933,
		note: 'Without Manchukuo, which took Jehol early in 1933; the Tanggu Truce of 31 May 1933 made the strip south of the Great Wall east of Peiping a demilitarised zone, which is not drawn separately.',
		source: 'chinaRemainder',
		coordinates: ring('roc1933'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},
	{
		id: 'roc-1934',
		name: 'Republic of China',
		kind: 'context',
		start: 1934,
		end: 1934,
		note: 'As for 1933, without the banner lands under the Mongolian Political Affairs Council, inaugurated at Bailingmiao on 23 April 1934 with the Nanjing government’s sanction (drawn separately). The leagues stayed formally inside the provinces of Chahar and Suiyuan.',
		source: 'chinaRemainder',
		coordinates: ring('roc1934'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},
	{
		id: 'roc-1935',
		name: 'Republic of China',
		kind: 'context',
		start: 1935,
		end: 1935,
		note: 'As for 1934, without the Mongolian Political Affairs Council’s leagues (drawn separately). The He–Umezu and Qin–Doihara agreements of June 1935 withdrew Chinese government forces from Hebei and Chahar; the Hebei–Chahar Political Council of December 1935 governed both provinces under Song Zheyuan, within the Republic (not drawn separately).',
		source: 'chinaRemainder',
		coordinates: ring('roc1935'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},
	{
		id: 'roc-1936',
		name: 'Republic of China',
		kind: 'context',
		start: 1936,
		end: 1936,
		note: 'Without the Mongolian Military Government (founded May 1936) and the East Hebei Autonomous Council.',
		source: 'chinaRemainder',
		coordinates: ring('roc1936'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},
	{
		id: 'roc-1937',
		name: 'Republic of China',
		kind: 'context',
		start: 1937,
		end: 1937,
		note: 'As for 1936, with the Military Government’s smaller 1937 area. The war with Japan began on 7 July 1937, after this year’s 1 July.',
		source: 'chinaRemainder',
		coordinates: ring('roc1937'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},
	{
		id: 'roc-1938',
		name: 'Republic of China',
		kind: 'context',
		start: 1938,
		end: 1939,
		note: 'Without the Mongol governments and the provinces of north China claimed by the Japanese-sponsored Provisional Government (founded at Peking on 14 December 1937). The Nationalist government had moved to Hankou and then Chongqing; in the north it kept forces behind Japanese lines, as did the Chinese Communists.',
		source: 'chinaRemainder',
		coordinates: ring('roc1938'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},
	{
		id: 'roc-1940',
		name: 'Republic of China',
		kind: 'context',
		start: 1940,
		end: 1941,
		note: 'As for 1938–1939; from 30 March 1940 the north China provinces were under Wang Jingwei’s Reorganized National Government, through the North China Political Council.',
		source: 'chinaRemainder',
		coordinates: ring('roc1940'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},
	{
		id: 'roc-1942',
		name: 'Republic of China',
		kind: 'context',
		start: 1942,
		end: 1945,
		note: 'As for 1940–1941, with Outer Mongolia’s line of 1941 at Khalkhin Gol.',
		source: 'chinaRemainder',
		coordinates: ring('roc1942'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},
	{
		id: 'roc-1946',
		name: 'Republic of China',
		kind: 'context',
		start: 1946,
		end: 1949,
		note: 'After Japan’s surrender the Republic took back Manchuria, Inner Mongolia and Taiwan, and in January 1946 recognised Outer Mongolia’s independence. The civil war is not drawn: Communist forces held much of Manchuria and the countryside of north China from 1946, all of Manchuria from November 1948 and Peiping from January 1949, so for 1948 and 1949 the area overstates what the Nationalist government held. The Inner Mongolian Autonomous Government (May 1947), under the Communists, is not yet drawn. The Kwantung peninsula, Chinese in law, stayed under Soviet occupation, drawn over it.',
		source: 'chinaRemainder',
		coordinates: ring('roc1946'),
		label: [108.4, 36.4],
		labelName: 'Republic\nof China',
		color: C.roc,
		legendName: 'Republic of China',
	},
	{
		id: 'prc-1950',
		name: 'People’s Republic of China',
		kind: 'context',
		start: 1950,
		end: 1950,
		note: 'The People’s Republic of China was proclaimed on 1 October 1949. Same outline as 1946–1949; the Republic of China held Taiwan, outside this map.',
		source: 'chinaRemainder',
		coordinates: ring('roc1946'),
		label: [108.4, 36.4],
		labelName: 'People’s Republic\nof China',
		color: C.prc,
		legendName: 'People’s Republic of China',
	},
	{
		id: 'east-hebei',
		name: 'East Hebei Autonomous Council',
		kind: 'context',
		start: 1936,
		end: 1937,
		note: 'Set up by Yin Rugeng (Yin Jukeng) under Japanese sponsorship in the demilitarised zone east of Peiping on 25 November 1935 (renamed the East Hebei Autonomous Government that December) and merged into the Provisional Government on 1 February 1938, so it is drawn for 1936 and 1937. Outline from Narangoa and Cribb’s 1935–1940 map, carried south to the coast where the plate’s lettering covers it. Not yet an atlas entry.',
		source: 'nc2014',
		coordinates: ring('eastHebei'),
		label: [118.6, 40.05],
		labelName: 'East\nHebei',
		color: C.eastHebei,
	},


	{
		id: 'provisional-government',
		name: 'Provisional Government of the Republic of China (Japanese-sponsored)',
		kind: 'context',
		start: 1938,
		end: 1939,
		note: 'Founded at Peking on 14 December 1937 under Japanese sponsorship, with Wang Kemin at its head; it absorbed the East Hebei government on 1 February 1938 and was merged into Wang Jingwei’s Reorganized National Government on 30 March 1940, so it is drawn for 1938 and 1939. It nominally governed the provinces of Hebei, Shandong, Shanxi, Henan and Jiangsu, with Peking and Tianjin; its real authority ran in the larger cities and along the railways, where Japanese troops were permanently stationed, while Chinese Communist and Nationalist forces held much of the countryside (Boyle, China and Japan at War, 1972, pp. 83–91, as summarised by Wikipedia, “Provisional Government of the Republic of China (1937–1940),” read October 2026). The area is drawn as those provinces, which is the government’s claim: in mid-1938 the southern part of Shanxi and Henan south of the Yellow River were still contested or Chinese-held. Jiangsu lies south of this map. Not yet an atlas entry.',
		source: 'northChinaProvinces',
		coordinates: ring('northChina1938'),
		label: [115.5, 37.4],
		labelName: 'Provisional\nGovernment',
		color: C.collab,
	},
	{
		id: 'reorganized-government',
		name: 'Reorganized National Government of the Republic of China (Wang Jingwei)',
		kind: 'context',
		start: 1940,
		end: 1945,
		note: 'Proclaimed at Nanjing on 30 March 1940 under Wang Jingwei, with Japanese sponsorship. In the north it governed through the North China Political Council at Peking, the Provisional Government under a new name, which kept much of its autonomy until the end of the war (Wikipedia, citing Li 2007). Mengjiang was nominally part of it but kept its own government and is drawn separately. Drawn as the provinces the Council governed, Hebei, Shandong, Shanxi and Henan (see the Provisional Government’s note on what this overstates). Dissolved after Japan’s surrender in August 1945. Not yet an atlas entry.',
		source: 'northChinaProvinces',
		coordinates: ring('northChina1940'),
		label: [115.5, 37.4],
		labelName: 'Reorganized\nNational Government',
		color: C.collab,
		legendName: 'Reorganized National Government (Wang Jingwei)',
	},
	{
		id: 'joseon',
		name: 'Joseon (Korea)',
		kind: 'context',
		start: 1890,
		end: 1897,
		note: 'The Joseon kingdom, a tributary of the Qing until the Treaty of Shimonoseki (April 1895) ended that tie. King Gojong proclaimed the Korean Empire on 12 October 1897, so 1897 is still drawn as Joseon.',
		source: 'koreaRivers',
		coordinates: T0('korea'),
		parts: TP('korea'),
		label: [126.3, 40.3],
		labelName: 'Joseon',
		stateName: 'Joseon (Korea)',
		color: C.korea,
		legendName: 'Joseon and the Korean Empire',
	},
	{
		id: 'korean-empire',
		name: 'Korean Empire',
		kind: 'context',
		start: 1898,
		end: 1910,
		note: 'Proclaimed on 12 October 1897. Japan made it a protectorate by the treaty of November 1905 and annexed it on 29 August 1910; on 1 July 1910 it still existed, so it is drawn to 1910.',
		source: 'koreaRivers',
		coordinates: T0('korea'),
		parts: TP('korea'),
		label: [126.3, 40.3],
		labelName: 'Korean\nEmpire',
		stateName: 'Korean Empire',
		color: C.korea,
		legendName: 'Joseon and the Korean Empire',
	},
	{
		id: 'korea-japan',
		name: 'Korea under Japan (Chōsen)',
		kind: 'context',
		start: 1911,
		end: 1945,
		note: 'Annexed by Japan on 29 August 1910 and ruled as the Government-General of Chōsen until Japan’s surrender in August 1945.',
		source: 'koreaRivers',
		coordinates: T0('korea'),
		parts: TP('korea'),
		label: [126.3, 40.3],
		labelName: 'Korea\n(Japan)',
		color: C.japan,
		legendName: 'Japanese Empire (Korea and the Kwantung Leased Territory)',
	},
	{
		id: 'korea-soviet',
		name: 'Korea under Soviet occupation',
		kind: 'context',
		start: 1946,
		end: 1948,
		note: 'North of the 38th parallel, occupied by Soviet troops from August 1945. The Democratic People’s Republic of Korea was proclaimed on 9 September 1948, so it is drawn from 1949.',
		source: 'koreaRivers',
		coordinates: T0('koreaNorth'),
		parts: TP('koreaNorth'),
		label: [126.4, 40.0],
		labelName: 'Soviet\nzone',
		color: C.russia,
		legendName: 'Soviet Union',
	},
	{
		id: 'korea-us',
		name: 'Korea under American occupation',
		kind: 'context',
		start: 1946,
		end: 1948,
		note: 'South of the 38th parallel, occupied by American troops from September 1945. The Republic of Korea was proclaimed on 15 August 1948, so it is drawn from 1949.',
		source: 'koreaRivers',
		coordinates: T0('koreaSouth'),
		parts: TP('koreaSouth'),
		label: [127.0, 36.6],
		labelName: 'US\nzone',
		stateName: 'United States (occupation of southern Korea)',
		color: C.usZone,
	},
	{
		id: 'dprk',
		name: 'Democratic People’s Republic of Korea',
		kind: 'context',
		start: 1949,
		end: 1950,
		note: 'Proclaimed on 9 September 1948, north of the 38th parallel. Its army crossed the parallel on 25 June 1950 and took Seoul on 28 June, so on 1 July 1950 the front lay south of the line drawn; the war’s fronts are not drawn.',
		source: 'koreaRivers',
		coordinates: T0('koreaNorth'),
		parts: TP('koreaNorth'),
		label: [126.4, 40.0],
		labelName: 'North\nKorea',
		color: C.dprk,
	},
	{
		id: 'rok',
		name: 'Republic of Korea',
		kind: 'context',
		start: 1949,
		end: 1950,
		note: 'Proclaimed on 15 August 1948, south of the 38th parallel (see North Korea’s note on 1950).',
		source: 'koreaRivers',
		coordinates: T0('koreaSouth'),
		parts: TP('koreaSouth'),
		label: [127.0, 36.6],
		labelName: 'South\nKorea',
		color: C.rok,
	},
	{
		id: 'kwantung-russia',
		name: 'Kwantung Leased Territory (Russia)',
		kind: 'context',
		start: 1898,
		end: 1904,
		note: 'Leased by Russia from the Qing in March 1898 for 25 years, with Port Arthur (Lüshun) and Dalny (Dalian) (Wikipedia, “Kwantung Leased Territory,” read October 2026). The lease stayed Russian in law until the Treaty of Portsmouth of 5 September 1905 passed it to Japan, so it is drawn as Russian through 1905; for 1905 Japanese occupation is drawn over it, since Japan had taken Port Arthur on 2 January 1905. The Russian lease’s exact boundary is not traced; the Japanese one is drawn. (Japan had also held the Liaodong peninsula in 1894–1895, until the Triple Intervention, which is not drawn.)',
		source: 'kwantung1934',
		coordinates: T0('kwantung'),
		parts: TP('kwantung'),
		label: [121.75, 39.2],
		labelName: 'Dalny\n(Russia)',
		stateName: 'Russian Empire (Kwantung lease)',
		color: C.russia,
	},
	{
		id: 'kwantung-russia-1905',
		name: 'Kwantung Leased Territory (Russia)',
		kind: 'context',
		start: 1905,
		end: 1905,
		note: 'Leased by Russia from the Qing in March 1898 for 25 years, with Port Arthur (Lüshun) and Dalny (Dalian) (Wikipedia, “Kwantung Leased Territory,” read October 2026). The lease stayed Russian in law until the Treaty of Portsmouth of 5 September 1905 passed it to Japan, so it is drawn as Russian through 1905; for 1905 Japanese occupation is drawn over it, since Japan had taken Port Arthur on 2 January 1905. The Russian lease’s exact boundary is not traced; the Japanese one is drawn. (Japan had also held the Liaodong peninsula in 1894–1895, until the Triple Intervention, which is not drawn.)',
		source: 'kwantung1934',
		coordinates: T0('kwantung'),
		parts: TP('kwantung'),
		stateName: 'Russian Empire (Kwantung lease)',
		color: C.russia,
	},
	{
		id: 'kwantung-japan-1905',
		name: 'Kwantung, Russian lease under Japanese occupation',
		kind: 'occupied',
		start: 1905,
		end: 1905,
		note: 'Japanese troops held the peninsula on 1 July 1905: Port Arthur had surrendered on 2 January 1905. The lease was still Russian in law until the Treaty of Portsmouth of 5 September 1905, so the occupation is drawn over the Russian lease.',
		source: 'kwantung1934',
		coordinates: T0('kwantung'),
		parts: TP('kwantung'),
		label: [121.75, 39.2],
		labelName: 'Dalny\n(Russian, held by Japan)',
		color: C.japan,
		legendName: 'Japanese occupation (Kwantung)',
	},
	{
		id: 'kwantung-japan',
		name: 'Kwantung Leased Territory (Japan)',
		kind: 'context',
		start: 1906,
		end: 1945,
		note: 'Leased to Japan under the Treaty of Portsmouth (5 September 1905) until Japan’s surrender in 1945; its administrative seat was Port Arthur (Ryojun), and its port Dairen (Dalian). The Kwantung Garrison that guarded it was renamed the Kwantung Army in 1919 (Wikipedia, “Kwantung Leased Territory”). Boundary from the 1934 Manchukuo map.',
		source: 'kwantung1934',
		coordinates: T0('kwantung'),
		parts: TP('kwantung'),
		label: [121.75, 39.2],
		labelName: 'Dairen\n(Japan)',
		color: C.japan,
		legendName: 'Japanese Empire (Korea and the Kwantung Leased Territory)',
	},
	{
		id: 'kwantung-china-1946',
		name: 'Port Arthur and Dalian (Republic of China, under Soviet occupation)',
		kind: 'context',
		start: 1946,
		end: 1949,
		note: 'Chinese territory after Japan’s surrender, but held by Soviet troops (see the Soviet occupation drawn over it).',
		source: 'kwantung1934',
		coordinates: T0('kwantung'),
		parts: TP('kwantung'),
		stateName: 'Republic of China',
		color: C.roc,
		legendName: 'Republic of China',
	},
	{
		id: 'kwantung-china-1950',
		name: 'Port Arthur and Dalian (People’s Republic of China, under Soviet occupation)',
		kind: 'context',
		start: 1950,
		end: 1950,
		note: 'Chinese territory, held by Soviet troops until 1955 (see the Soviet occupation drawn over it).',
		source: 'kwantung1934',
		coordinates: T0('kwantung'),
		parts: TP('kwantung'),
		stateName: 'People’s Republic of China',
		color: C.prc,
		legendName: 'People’s Republic of China',
	},
	{
		id: 'kwantung-soviet',
		name: 'Port Arthur and Dalian under Soviet occupation',
		kind: 'occupied',
		start: 1946,
		end: 1950,
		note: 'Soviet troops took the peninsula in August 1945 and began to administer it in September (Wikipedia, “Kwantung Leased Territory”). The Sino-Soviet treaty of 14 August 1945 made Port Arthur a joint naval base and Dalian a free port. The territory stayed under Soviet occupation until the Lüshun base was handed over to the People’s Republic of China on 16 April 1955 (Wikipedia), beyond this map’s last year.',
		source: 'kwantung1934',
		coordinates: T0('kwantung'),
		parts: TP('kwantung'),
		label: [121.75, 39.2],
		labelName: 'Dalian\n(Soviet occupation)',
		color: C.soviet,
		legendName: 'Soviet occupation (Port Arthur and Dalian)',
	},
	{
		id: 'impr-1945',
		name: 'Inner Mongolian People’s Republic (provisional government)',
		entry: 'inner-mongolian-republican-provisional-government',
		labelName: 'Inner Mongolian\nPeople’s Republic\n(Sept–Oct 1945)',
		kind: 'claimed',
		start: 1945,
		end: 1945,
		note: 'The Provisional Government of the Inner Mongolian People’s Republic, proclaimed at a congress at the Öndör monastery in Sünid Right Banner that opened on 9 September 1945, after Mongolia refused to unite with Inner Mongolia; it was renamed the Mongolian Autonomous Government under Yunze (Ulanhu) in October and dissolved itself in late October (Inner Mongolia gazetteer; see the entry). It is drawn on the 1945 map although it was founded after 1 July, like the campaigns of the year. Its claimed territory is not known from a source in hand: the declaration and constitution (published by Tabuchi Yōko, 2008) have not been seen. Drawn instead are the leagues represented at its congress: delegates came from the Shilingol banners, seven Chahar banners (all but Plain Blue and Taipusi Left) and the Dörben Keüked banner of Ulanchab. Outline: the Shilingol and Chahar leagues as the Nakamura (1941) map draws them, so it includes the two Chahar banners that were not represented and leaves out Dörben Keüked, which cannot be separated at league scale.',
		source: 'nakamura1941',
		coordinates: ring('impr1945'),
		label: [113.6, 43.6],
		color: C.impr,
		legendName: 'Inner Mongolian People’s Republic (leagues at its congress, Sept–Oct 1945)',
	},	{
		id: 'empag-1946',
		entry: 'east-mongolian-peoples-autonomous-government',
		name: 'East Mongolian People’s Autonomous Government',
		labelName: 'East Mongolian People’s\nAutonomous Government\n(Jan–May 1946)',
		kind: 'claimed',
		start: 1946,
		end: 1946,
		note: 'The East Mongolian People’s Autonomous Government, founded at a congress of representatives of 36 eastern banners at Gegeen Süme from 16 January 1946, with Boyanmandu as chairman and Khafungga as secretary-general; its provinces were Hinggan, Jirim, Juu Uda, Josotu, Hulunbuir and Nawen Muren (Chinese Wikipedia, “東蒙古人民自治政府,” read October 2026). The Chengde talks of 3 April 1946 agreed to dissolve it, and a congress at Wangyemiao declared it abolished on 27 May 1946 (same). A US memorandum of 30 July 1947 notes that its January 1946 proclamation had no known sanction from the Chinese Government and that its laws, though framed as autonomy under Chinese sovereignty, “savor more of independence” (Sprouse to Wedemeyer, FRUS 1947, vol. VII). It is drawn on the 1946 map although it was dissolved before 1 July, so that it appears at all. Outline: the banner lands of the Jirim, Juu Uda and Josotu leagues (the Hinggan banners lay within Jirim) as the 1930s English banner map draws their outer boundary, read from points along its lines (10–26 km), with Hulunbuir on its 1912 outline; the Chinese counties among the banners are not separated out. Nawen Muren, the Butha banners along the Nonni, has no outline in hand and is not drawn. Hulunbuir also had its own autonomous provincial government in 1945–1946 (the Inner Mongolia gazetteer gives it a section of its own), which is not drawn separately.',
		source: 'bannerMap1930s',
		coordinates: ring('empag1946'),
		label: [121.2, 45.0],
		color: C.mongol,
		legendName: 'East Mongolian People’s Autonomous Government (Jan–May 1946)',
	},
];

/**
 * The Great Wall, drawn in every year as a landmark. Traced from the Nakamura
 * (1941) map, which draws the Wall from Shanhaiguan to the Ningxia corner of the
 * Ordos; it does not show the Wall farther west, so none is drawn there.
 */
export const greatWallLines = greatWall.greatWall as [number, number][][];
export const greatWallSource = areaSources.nakamura1941;

/**
 * Military campaigns drawn as routes. A route shows a direction of advance as
 * the sources give it, not a front line or territory held. Its tail is placed
 * where the sources say the force set out, as closely as they allow; `tailNote`
 * says how exact that is.
 */
export interface CampaignRoute {
	label: string;
	from: [number, number];
	to: [number, number];
	note: string;
}

export interface CampaignPlace {
	name: string;
	at: [number, number];
	note: string;
}

export interface Campaign {
	id: string;
	name: string;
	/** Atlas entry the campaign links to, once there is one. */
	entry?: string;
	start: number;
	end: number;
	tailNote: string;
	source: string;
	routes: CampaignRoute[];
	/** Places the force occupied, drawn as markers; with a note on what is left unplaced. */
	reached?: CampaignPlace[];
	reachedNote?: string;
}

// Starting areas. Neither source gives coordinates.
const DARIGANGA: [number, number] = [113.85, 45.31]; // present-day Dariganga sum centre, approximate
const TUSHEET_SOUTH: [number, number] = [109.0, 42.6]; // on the 1914 frontier south of Tüsheet Khan aimag; schematic

export const campaigns: Campaign[] = [
	{
		id: 'five-roads-1913',
		name: 'Five Roads campaign, 1913',
		entry: 'five-roads-campaign',
		start: 1913,
		end: 1913,
		tailNote: 'Mongoltoli names two starting areas: Dariganga with the Egüzer monastery, and the southern edge of Tüsheet Khan aimag. The eastern routes are drawn from Dariganga (its present-day sum centre, approximate) and the western ones from a schematic point on the frontier south of Tüsheet Khan aimag. The Egüzer monastery is probably the “Yegüzer Temple (Erdenetsagaan)” that Atwood lists among the MPR’s border stations in 1928 (Young Mongols and Vigilantes, p. 937), near present-day Erdenetsagaan, about 135 km east-north-east of Dariganga; no route is drawn from it yet.',
		source: 'Baabar, “Таван замын байлдаан” (Baabar.mn, 10 October 2026), and G. Myagmarsambuu, “Таван замын байлдаан,” Mongoltoli (mongoltoli.mn). Route names from Baabar; starting areas from Mongoltoli. Places occupied: Atwood, Encyclopedia of Mongolia and the Mongol Empire (2004), “Sino-Mongolian War”; the Dolonnor thrust also from Jagchid, The Last Mongol Prince (1999), p. 15. Pangjiang’s position: China News Service (2017), see its marker.',
		reached: [
			{ name: 'Linxi', at: [118.067, 43.617], note: 'Occupied at the furthest advance (Atwood). Position: Linxi County as Wikipedia gives it (read October 2026).' },
			{ name: 'Jingpeng (Kheshigten Banner)', at: [117.48, 43.28], note: 'Atwood names Kheshigten Banner and Jingpeng, its seat. Position: Hexigten Banner as Wikipedia gives it (read October 2026).' },
			{ name: 'Outskirts of Dolonnor', at: [116.48, 42.2], note: 'Atwood: the outskirts of Dolonnuur (Duolun), not the town. Jagchid says a force under Shirun jiangjun and Namsarai bagatur was sent to take Doloonnor but withdrew under Chinese pressure before it could, after which the Chinese occupied the town and killed the Kanjurwa Khutugtu (p. 15). Marker at the town, as on the rest of this map.' },
			{ name: 'Bailingmiao (Batu-Khaalga)', at: [110.435, 41.7], note: 'Occupied at the furthest advance (Atwood). Position as in the Bailingmiao entry.' },
			{ name: 'Pangjiang (Ming’an)', at: [112.851, 42.582], note: 'Occupied at the furthest advance (Atwood). Pangjiang, also called Ming’an, was a station on the Kalgan–Urga road. Position: about 25 km southeast of Saihantala, the Sünid Right Banner seat, as a China News Service report gives it (“在苏尼特右旗，曾经有个地方叫滂江,” 20 November 2017), taking Saihantala at 42.741° N, 112.635° E (Mapcarta); the report’s distance is approximate. Jagchid instead puts Pangjiang “about fifty kilometers southeast of the residence of the Sunid prince” (p. 16). That residence, De Wang’s palace (now the Sünid palace museum, placed on this map), stands about 16 km south-south-east of this point, so the two accounts disagree on direction and distance. Both are recorded; the marker follows the report, which gives a position, while Jagchid gives only a bearing from a point.' },
			{ name: 'Dashetai', at: [109.14, 41.036], note: 'Occupied at the furthest advance (Atwood, “Sino-Mongolian War”). Atwood elsewhere describes Dashetai (Yekhe Sheetei) as a Chinese farming settlement in Urad Right Duke Banner, north of Muna Uula (Wula Shan), with Ulaan Khuddug to its east (Atwood 2002, pp. 603, 842), which identifies it with present-day Dashetai (大佘太) in Urad Front Banner. Position: read from Atwood’s Map 15.1 (“Alashan and Western Inner Mongolia, 1927–1928,” Young Mongols and Vigilantes), fitted to 15 towns on that map; checked by leaving each town out in turn, the fit places towns typically within about 6 km and at worst about 15 km here. Approximate.' },
			{ name: 'Ulaan Oboo', at: [108.568, 41.238], note: 'Occupied at the furthest advance (Atwood, “Sino-Mongolian War”). Position: the Ulaan Oboo on Atwood’s Map 15.1 (Young Mongols and Vigilantes, 1927–1928), between Wuyuan and Dashetai in Urad Right Duke Banner, fitted as for Dashetai. Ulaan Oboo (“red cairn”) is a common place name, and Atwood does not say this is the Ulaan Oboo of his 1913 list; the identification rests on the same author placing it beside Dashetai, the next name on that list. Approximate.' },
		],
		reachedNote: 'Atwood lists the places the Mongolian troops occupied at their furthest advance, in summer and autumn 1913, before Russia ordered the campaign stopped on 28 October. Erfenzi is also on his list but is not yet placed, since no position for it has been sourced. Dashetai and Ulaan Oboo are placed from Atwood’s own map of western Inner Mongolia in 1927–1928. When each place was taken is not given, so the markers show the campaign as a whole, not 1 July 1913.',
		routes: [
			{ label: 'Чуулалт хаалга (Kalgan)', from: DARIGANGA, to: [114.88, 40.82], note: 'Baabar’s first route, “Kalgan and the western part.” Mongoltoli sends the eastern force toward Chahar.' },
			{ label: 'Долоннуур (Dolonnor)', from: DARIGANGA, to: [116.48, 42.2], note: 'Mongoltoli: Damdinsüren and Sumiya led the eastern force toward Shilingol, Juu Uda, Chahar and Dolonnor.' },
			{ label: 'Хөх хот (Hohhot)', from: TUSHEET_SOUTH, to: [111.66, 40.82], note: 'Mongoltoli: Sonomdorj and Chagdarjav led the western force toward Ulaanchab and Hohhot. Baabar: an attack on Hohhot on 7 July 1913 with over a thousand men was beaten back.' },
			{ label: 'Бугат (Baotou)', from: TUSHEET_SOUTH, to: [110.05, 40.59], note: 'Baabar: the route to Baotou along the Хатан гол (Yellow River), under Sumiya, whom Mongoltoli places with the eastern force instead.' },
			{ label: 'Бат хаалга (Bailingmiao)', from: TUSHEET_SOUTH, to: [110.435, 41.7], note: 'Baabar: Bat khaalga, in Darkhan Muumingan banner; this is the atlas’s Bat-khaalag, Bailingmiao.' },
		],
	},
	{
		id: 'manchuria-1945',
		name: 'Soviet–Mongolian invasion of Manchuria and Inner Mongolia, August 1945',
		start: 1945,
		end: 1945,
		tailNote: 'Mongolian and Transbaikal starting points are read off the Soviet map’s arrows (about 10–20 km): the Soviet–Mongolian group from Moltsog Khiid and Dzamyn-Üüd, the 17th Army from Yugodzyr (Egüzer) Khiid, the 53rd Army from its assembly area west of Tamsag-Bulag, the 6th Guards Tank Army from the south side of the Tamsag-Bulag salient and the 39th Army from its tip. The 36th Army starts at Staro-Tsurukhaitui on the Argun, the 2nd Red Banner Army at Blagoveshchensk, the 15th Army at Leninskoye on the Amur and the 1st Far Eastern Front at Grodekovo; the last three lie at or beyond this map’s eastern edge. Arrows for the Far Eastern Fronts are drawn only where they reach this map.',
		source: 'Soviet map “Маньчжурская наступательная операция 9 августа – 2 сентября 1945 г.” (1:14,000,000; publication not yet identified), read for directions and starting points only, with a quadratic fit to 19 towns (typically 5–20 km); and an English-language map of the invasion sent by the atlas maintainer (Wikimedia Commons; author not recorded), which draws the same axes. Both draw the post-1962 Sino-Soviet and Sino-Mongolian borders, which are not used: the borders on this map are the atlas’s own. Events and dates: Russian Wikipedia, “Маньчжурская операция (1945)” and “Хингано-Мукденская операция” (read October 2026), citing История Второй мировой войны 1939–1945, vol. 11 (1979); English Wikipedia, “Soviet invasion of Manchuria” (read October 2026), citing Glantz, August Storm (Leavenworth Papers 7, 1983); for the Soviet–Mongolian group, V. G. Datsyshen interviewed by A. Tarasov, “Советско-японская война 1945 г.: Советско-монгольское братство по оружию,” Chita.ru, 25 July 2021.',
		routes: [
			{ label: '36th Army: Hailar', from: [119.32, 50.25], to: [119.73, 49.21], note: 'Crossed the Argun on 9 August and took the town of Hailar on 11 August; the Hailar fortified district held out until 18 August (Russian and English Wikipedia).' },
			{ label: '36th Army: Qiqihar', from: [119.73, 49.21], to: [123.97, 47.34], note: 'From Hailar over the Greater Khingan by Bukhedu and Zhalantun to Qiqihar, which lies on the line the fronts had reached by 19 August (Russian Wikipedia; Soviet map).' },
			{ label: '39th Army: Wangyemiao and Solun', from: [119.39, 47.25], to: [122.07, 46.08], note: 'From the tip of the Tamsag-Bulag salient, bypassing the Halun-Arshan fortified district, the 39th Army took Wangyemiao (Ulanhot) and Solun on 13 August, then pressed on toward Tao’an and Taonan (Russian Wikipedia).' },
			{ label: '39th Army: Changchun', from: [122.07, 46.08], to: [125.32, 43.88], note: 'By Taonan toward Changchun, as the Soviet map draws it. Changchun (Xinjing), Manchukuo’s capital, also received a Soviet airborne landing between 18 and 27 August (Russian Wikipedia).' },
			{ label: '6th Guards Tank Army: Lubei', from: [118.48, 46.35], to: [120.9, 44.56], note: 'The armoured spearhead crossed the Greater Khingan and took Lubei (Jarud) on 11 August, then was held up near Lubei and Tuquan for about two days until fuel was flown in (Russian Wikipedia).' },
			{ label: '6th Guards Tank Army: Changchun', from: [120.9, 44.56], to: [125.32, 43.88], note: 'Part of its forces turned on Changchun from 12 August (Russian Wikipedia).' },
			{ label: '6th Guards Tank Army: Mukden', from: [120.9, 44.56], to: [123.43, 41.8], note: 'Its main forces drove on Mukden (Shenyang, Fengtian), which an airborne landing seized on 19 August; it later went on to Port Arthur (Lüshun), beyond this map (Russian Wikipedia; English Wikipedia has Mukden reached by 20 August).' },
			{ label: '53rd Army: Kailu', from: [116.12, 47.15], to: [121.3, 43.6], note: 'Committed behind the 6th Guards Tank Army on 16 August with orders to reach the Kailu area; by the end of 26 August it stood on the Laoha and Liao rivers on the line Xinmiao, Kailu, Tongliao (Russian Wikipedia).' },
			{ label: '17th Army: Chifeng', from: [115.22, 45.46], to: [118.96, 42.27], note: 'Crossed the desert by 11 August and advanced on Chifeng (Russian Wikipedia). Starting point: Yugodzyr Khiid on the Soviet map, probably the Egüzer monastery named as a 1913 starting area, which Atwood lists as “Yegüzer Temple (Erdenetsagaan)” among the MPR’s border stations in 1928 (Young Mongols and Vigilantes, p. 937).' },
			{ label: '17th Army: Pingquan', from: [118.96, 42.27], to: [118.7, 41.01], note: 'After taking Chifeng its main forces concentrated around Pingquan and Lingyuan (Russian Wikipedia).' },
			{ label: 'Soviet–Mongolian group: Dolonnor', from: [113.73, 44.73], to: [116.48, 42.2], note: 'The group’s main blow, under I. A. Pliyev with the Mongolian general J. Lkhagvasüren as deputy; two Mongolian cavalry divisions were on this axis. On the morning of 14 August a regiment of the Soviet 59th Cavalry Division with two mechanised brigades took Dolonnor (Datsyshen). The Mongolian People’s Republic had declared war on Japan on 10 August.' },
			{ label: 'Soviet–Mongolian group: Jehol (Chengde)', from: [116.48, 42.2], to: [117.93, 40.97], note: 'The Dolonnor force reached Fengning on 18 August and Jehol (Chengde) the next day, where the Japanese garrison began to surrender on the evening of 19 August (Datsyshen, quoting the journal of the Mongolian army group).' },
			{ label: 'Soviet–Mongolian group: Kalgan', from: [111.9, 43.71], to: [114.88, 40.82], note: 'The supporting blow from Dzamyn-Üüd by Erlian and Zhangbei, where its main force fought at the town walls. Between 15 and 22 August Soviet and Mongolian troops took the Kalgan fortified district, but on 21 August they were ordered to stop the advance on Kalgan (Datsyshen). Who first held the city afterwards is not settled here. On 22 August the Mongolian 5th Cavalry Division was about 70 km from Peking.' },
			{ label: '2nd Red Banner Army: Qiqihar', from: [127.53, 50.26], to: [123.97, 47.34], note: '2nd Far Eastern Front. Crossed the Amur and took Sakhalyan (Heihe) and Aigun on the first day, broke the Sunwu fortified district on 12–14 August, and sent its main forces toward Qiqihar (Russian Wikipedia).' },
			{ label: '15th Army: Harbin', from: [132.97, 47.94], to: [126.63, 45.75], note: '2nd Far Eastern Front, up the Sungari with the Amur Flotilla from Leninskoye; Harbin was taken together with the 1st Far Eastern Front, with an airborne landing there from 18 August (Russian Wikipedia).' },
			{ label: '1st Far Eastern Front: Harbin and Jilin', from: [131.67, 44.4], to: [126.55, 43.84], note: 'From the Ussuri frontier by Mudanjiang, which the 5th Army reached on 14 August; the 10th Mechanized Corps pushed toward Jilin (Girin) from 12 August, and Jilin also received an airborne landing on 19 August (Russian Wikipedia). Only the end of this axis falls on this map.' },
		],
	},
];
