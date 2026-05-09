import { source } from "@/lib/source";

export const revalidate = false;

export function GET() {
	const body = source
		.getPages()
		.filter((page) => page.data.visibility !== "internal")
		.map((page) => `- ${page.data.title}: ${page.url}`)
		.join("\n");

	return new Response(`# shortcuts docs\n\n${body}\n`, {
		headers: { "Content-Type": "text/plain; charset=utf-8" },
	});
}
