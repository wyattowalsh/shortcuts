import { source } from "@/lib/source";

type Page = ReturnType<typeof source.getPages>[number];

export async function getLLMText(page: Page): Promise<string> {
	const processed = await page.data.getText("processed");
	return `# ${page.data.title}\n\nURL: ${page.url}\n\n${processed}`;
}
