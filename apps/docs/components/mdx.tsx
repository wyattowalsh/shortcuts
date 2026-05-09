import type { ComponentType } from "react";
import defaultMdxComponents from "fumadocs-ui/mdx";

export function getMDXComponents(
	components?: Record<string, ComponentType<unknown>>,
) {
	return {
		...defaultMdxComponents,
		...components,
	};
}
