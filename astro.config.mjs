// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
	redirects: {
		'/entry/united-committee-of-mengchiang': '/entry/united-committee-of-mengjiang',
		'/entry/west-sunit-ruling-house': '/entry/west-sunid-ruling-house',
	},
});
