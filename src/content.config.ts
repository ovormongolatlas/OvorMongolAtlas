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
		// life = birth-death; active = span of documented activity, not birth/death;
		// existed = an institution's founding-dissolution span; documented = earliest
		// to latest point documented in the cited sources (neither birth/death nor a
		// clean founding/dissolution, e.g. a still-standing city or a source's own
		// "as of" date). Themes omit startYear/endYear entirely rather than using a
		// yearType value, since no date range applies.
		yearType: z.enum(['life', 'active', 'existed', 'documented']).default('life'),
		// Entry id of the parent this entry is a successive stage of (e.g. the four
		// Mengjiang-era governments each set partOf: "mengjiang"), used to nest related
		// states in the entries index instead of listing them as flat overlapping peers.
		partOf: z.string().optional(),
	}),
});

export const collections = { entries };
