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
	}),
});

export const collections = { entries };
