export type YearType = 'life' | 'existed' | 'documented' | 'contested';

/**
 * Renders a startYear-endYear pair with a label reflecting what the dates mean,
 * so an activity span or a source's documented range is never mistaken for
 * birth-death dates. Returns null when either year is absent (theme entries),
 * rather than fabricating a range or printing "undefined"/"(–)".
 *
 * When startYear === endYear, renders just the one year rather than a
 * zero-width range (e.g. "documented 1898", not "documented 1898–1898").
 *
 * When yearType is 'contested', altStartYear/altEndYear (if present) are
 * joined to their endpoint with "or" and no qualifier word is prefixed: the
 * doubled year(s) are themselves the signal that the date is disputed. If
 * only one endpoint has an alternate, the other renders plainly.
 */
export function formatYearRange(
	startYear: number | undefined,
	endYear: number | undefined,
	yearType: YearType,
	altStartYear?: number,
	altEndYear?: number,
): string | null {
	if (startYear === undefined || endYear === undefined) return null;

	if (yearType === 'contested') {
		const start = altStartYear !== undefined ? `${startYear} or ${altStartYear}` : `${startYear}`;
		const end = altEndYear !== undefined ? `${endYear} or ${altEndYear}` : `${endYear}`;
		return `${start} – ${end}`;
	}

	const range = startYear === endYear ? `${startYear}` : `${startYear}–${endYear}`;
	switch (yearType) {
		case 'documented':
			return `documented ${range}`;
		case 'life':
		case 'existed':
		default:
			return range;
	}
}
