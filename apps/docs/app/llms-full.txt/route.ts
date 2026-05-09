import { getLLMText } from "@/lib/get-llm-text";
import { source } from "@/lib/source";

export const revalidate = false;

export async function GET() {
	const pages = source
		.getPages()
		.filter((page) => page.data.visibility !== "internal");
	const body = (await Promise.all(pages.map((page) => getLLMText(page)))).join(
		"\n\n---\n\n",
	);

	return new Response(body, {
		headers: { "Content-Type": "text/plain; charset=utf-8" },
	});
}
