import { metaSchema, pageSchema } from "fumadocs-core/source/schema";
import { defineConfig, defineDocs } from "fumadocs-mdx/config";
import { z } from "zod";

export const docs = defineDocs({
	dir: "content/docs",
	docs: {
		schema: pageSchema.extend({
			category: z.string().optional(),
			generated: z.boolean().default(false),
			index: z.boolean().default(true),
			source_artifact: z.string().optional(),
			visibility: z.enum(["public", "internal"]).default("public"),
		}),
		postprocess: {
			includeProcessedMarkdown: true,
		},
	},
	meta: {
		schema: metaSchema,
	},
});

export default defineConfig();
