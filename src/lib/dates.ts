export type YearType = 'life' | 'active' | 'existed' | 'documented';

/**
 * Renders a startYear-endYear pair with a label reflecting what the dates mean,
 * so an activity span or a source's documented range is never mistaken for
 * birth-death dates. Returns null when either year is absent (theme entries),
 * rather than fabricating a range or printing "undefined"/"(–)".
 */
export function formatYearRange(
	startYear: number | undefined,
	endYear: number | undefined,
	yearType: YearType,
): string | null {
	if (startYear === undefined || endYear === undefined) return null;

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
