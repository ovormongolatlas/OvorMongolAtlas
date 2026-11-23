import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const entries = defineCollection({
	loader: glob({ pattern: '**/*.md', base: './src/content/entries' }),
	schema: z.object({
		title: z.string(),
		// 'theme' covers cross-cutting thematic entries (e.g. a symbol or practice
		// traced across multiple actors and periods) that don't have a single
		// person/place/group/battle/state's natural start-end span.
		type: z.enum(['person', 'place', 'group', 'battle', 'state', 'theme']),
		summary: z.string(),
		// Optional because theme entries span too many actors and periods to have
		// a single meaningful start-end year; all other entry types still provide both.
		startYear: z.number().optional(),
		endYear: z.number().optional(),
		// What startYear/endYear represent, since the same two numbers mean very
		// different things across entries and must not all render as birth-death dates:
		// life = birth-death; existed = an institution's founding-dissolution span;
		// documented = earliest to latest point documented in the cited sources
		// (neither birth/death nor a clean founding/dissolution, e.g. a still-standing
		// city, a span of documented activity, or a source's own "as of" date);
		// contested = sources disagree on one or both endpoints, and altStartYear/
		// altEndYear hold the alternate attested value(s) so the header can display
		// the conflict instead of silently picking one. Themes omit startYear/endYear
		// entirely rather than using a yearType value, since no date range applies.
		yearType: z.enum(['life', 'documented', 'existed', 'contested']).default('life'),
		// Only meaningful when yearType is 'contested'; the alternate attested value
		// for startYear/endYear respectively. Leave unset if that endpoint isn't disputed.
		altStartYear: z.number().optional(),
		altEndYear: z.number().optional(),
		// Entry id of the parent this entry is a successive stage of (e.g. the four
		// Mengjiang-era governments each set partOf: "mengjiang"), used to nest related
		// states in the entries index instead of listing them as flat overlapping peers.
		partOf: z.string().optional(),
		// Where a place sits on the Timeline Map (src/pages/map.astro), in decimal
		// degrees (WGS84). Like every other claim in the atlas, a location carries
		// its source: `source` says where the coordinates come from and what they
		// stand for (e.g. a modern town centre standing in for a period settlement),
		// and `precision` is 'confirmed' only once checked against a source in hand,
		// otherwise 'approximate'. Places without a location are listed under the
		// map as not yet placed rather than being guessed.
		location: z
			.object({
				lat: z.number(),
				lon: z.number(),
				precision: z.enum(['approximate', 'confirmed']),
				source: z.string(),
			})
			.optional(),
		// Optional images with full attribution, rendered visibly on the entry page
		// (not just recorded here) because several of this atlas's held images carry
		// CC BY-ND terms requiring visible attribution, and public-domain images still
		// need their provenance stated. Do not crop, recolor, or otherwise alter any
		// image whose license/attribution block is recorded here without updating that
		// block to match, since some licenses (e.g. ND) forbid derivative alteration
		// outright. `src` is a path under /public (e.g. "/images/foo.jpg"), or a IIIF
		// image URL from an institution whose licence allows reuse (the Berlin banner
		// maps are loaded this way from the Staatsbibliothek's server); every other
		// field is free text so each institution's own cataloguing language can be used
		// as given rather than forced into a fixed vocabulary.
		// A short role line for the page header (e.g. "Mongol prince"). Falls back to
		// the entry type when unset.
		role: z.string().optional(),
		// The subject's name in other scripts, shown in the page header. Each name
		// carries its provenance, as the project notes require: `mongolianStatus` is
		// 'sourced' only when the traditional-script spelling has been checked against
		// a source in hand (named in `mongolianSource`); 'converter' marks a spelling
		// drafted with a script converter such as Kimo (kimo.mngl.net) and not yet
		// checked; 'unverified' marks any other unchecked draft. The status is shown
		// in the page's "At a glance" box.
		names: z
			.object({
				mongolian: z.string().optional(),
				mongolianStatus: z.enum(['sourced', 'converter', 'unverified']).optional(),
				mongolianSource: z.string().optional(),
				cyrillic: z.string().optional(),
				chinese: z.string().optional(),
				chineseSource: z.string().optional(),
			})
			.optional(),
		images: z
			.array(
				z.object({
					src: z.string(),
					alt: z.string(),
					// Show this image in the page header as well. It is shown whole (never
					// cropped), because some licenses recorded here forbid alteration; the
					// full attribution stays with the figure in the text, linked from the header.
					portrait: z.boolean().optional(),
					caption: z.string().optional(),
					photographer: z.string().optional(),
					depicted: z.string().optional(),
					date: z.string().optional(),
					venue: z.string().optional(),
					collection: z.string().optional(),
					institution: z.string().optional(),
					shelfmark: z.string().optional(),
					license: z.string().optional(),
					licenseUrl: z.string().optional(),
					source: z.string().optional(),
					note: z.string().optional(),
				}),
			)
			.optional(),
	}),
});

export const collections = { entries };
