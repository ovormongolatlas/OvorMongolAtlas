/**
 * Places a longitude/latitude on the Timeline Map's base image
 * (public/map/base.svg) as a percentage of the image's width and height.
 *
 * The projection is Lambert conformal conic on the WGS84 ellipsoid
 * (standard parallels 37°N and 47°N, origin 43°N 113°E), and the frame is the
 * window the base map was cut to. Both MUST match
 * scripts/basemap/make_basemap.py exactly, or markers will drift off the
 * rivers and coastlines drawn in the image. If you change one, change both
 * and regenerate the image.
 */

const A = 6378137; // WGS84 semi-major axis, metres
const F = 1 / 298.257223563;
const E = Math.sqrt(2 * F - F * F);

const LAT1 = 37;
const LAT2 = 47;
const LAT0 = 43;
const LON0 = 113;

const rad = (deg: number) => (deg * Math.PI) / 180;

const m = (phi: number) => Math.cos(phi) / Math.sqrt(1 - E * E * Math.sin(phi) ** 2);
const t = (phi: number) =>
	Math.tan(Math.PI / 4 - phi / 2) / ((1 - E * Math.sin(phi)) / (1 + E * Math.sin(phi))) ** (E / 2);

const m1 = m(rad(LAT1));
const m2 = m(rad(LAT2));
const t1 = t(rad(LAT1));
const t2 = t(rad(LAT2));
const N = (Math.log(m1) - Math.log(m2)) / (Math.log(t1) - Math.log(t2));
const BIG_F = m1 / (N * t1 ** N);
const RHO0 = A * BIG_F * t(rad(LAT0)) ** N;

function lcc(lon: number, lat: number): [number, number] {
	const rho = A * BIG_F * t(rad(lat)) ** N;
	const theta = N * rad(lon - LON0);
	return [rho * Math.sin(theta), RHO0 - rho * Math.cos(theta)];
}

// Frame of the base image, in projected metres (see make_basemap.py).
const [X_MIN] = lcc(96.0, 44);
const [X_MAX] = lcc(127.8, 44);
const [, Y_MAX] = lcc(113, 51.6);
const [, Y_MIN] = lcc(113, 35.3);

/** Width and height of public/map/base.svg, for the <img> width/height attributes. */
export const BASE_MAP_WIDTH = 1600;
export const BASE_MAP_HEIGHT = Math.round(((Y_MAX - Y_MIN) * BASE_MAP_WIDTH) / (X_MAX - X_MIN));

/** Position of a point on the base map, as percentages from the top-left corner. */
export function mapPosition(lon: number, lat: number): { left: number; top: number } {
	const [x, y] = lcc(lon, lat);
	return {
		left: (100 * (x - X_MIN)) / (X_MAX - X_MIN),
		top: (100 * (Y_MAX - y)) / (Y_MAX - Y_MIN),
	};
}

/** True when a point falls inside the base map's frame. */
export function isOnMap(lon: number, lat: number): boolean {
	const { left, top } = mapPosition(lon, lat);
	return left >= 0 && left <= 100 && top >= 0 && top <= 100;
}
