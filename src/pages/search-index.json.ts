import { getCollection } from 'astro:content';

export async function GET() {
	const entries = await getCollection('entries');
	const index = entries.map((entry) => ({
		id: entry.id,
		title: entry.data.title,
		type: entry.data.type,
		summary: entry.data.summary,
	}));

	return new Response(JSON.stringify(index), {
		headers: { 'Content-Type': 'application/json' },
	});
}
