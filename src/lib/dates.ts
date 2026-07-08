export type YearType = 'life' | 'active' | 'existed' | 'documented';

/**
 * Renders a startYear-endYear pair with a label reflecting what the dates mean,
 * so an activity span or a source's documented range is never mistaken for
 * birth-death dates.
 */
export function formatYearRange(startYear: number, endYear: number, yearType: YearType): string {
	const range = `${startYear}–${endYear}`;
	switch (yearType) {
		case 'active':
			return `active ${range}`;
		case 'documented':
			return `documented ${range}`;
		case 'life':
		case 'existed':
		default:
			return range;
	}
}
