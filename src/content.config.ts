import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const entries = defineCollection({
	loader: glob({ pattern: '**/*.md', base: './src/content/entries' }),
	schema: z.object({
		title: z.string(),
		type: z.enum(['person', 'place', 'group', 'battle', 'state']),
		summary: z.string(),
		startYear: z.number(),
		endYear: z.number(),
		// What startYear/endYear represent, since the same two numbers mean very
		// different things across entries and must not all render as birth-death dates:
		// life = birth-death; active = span of documented activity, not birth/death;
		// existed = an institution's founding-dissolution span; documented = earliest
		// to latest point documented in the cited sources (neither birth/death nor a
		// clean founding/dissolution, e.g. a still-standing city or a source's own
		// "as of" date).
		yearType: z.enum(['life', 'active', 'existed', 'documented']).default('life'),
		// Entry id of the parent this entry is a successive stage of (e.g. the four
		// Mengjiang-era governments each set partOf: "mengjiang"), used to nest related
		// states in the entries index instead of listing them as flat overlapping peers.
		partOf: z.string().optional(),
	}),
});

export const collections = { entries };
