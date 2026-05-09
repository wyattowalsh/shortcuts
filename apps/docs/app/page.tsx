import Link from "next/link";

export default function HomePage() {
	return (
		<main className="mx-auto flex min-h-screen max-w-5xl flex-col gap-8 px-6 py-20">
			<section className="space-y-4">
				<p className="text-sm font-medium uppercase tracking-wide text-fd-muted-foreground">
					shortcuts
				</p>
				<h1 className="text-4xl font-semibold tracking-tight">
					Source-controlled Apple Shortcuts and App Intents.
				</h1>
				<p className="max-w-2xl text-lg text-fd-muted-foreground">
					Developer-grade manifests, security review, catalog generation,
					release metadata, and docs for maintainable Shortcuts.
				</p>
			</section>
			<nav className="flex flex-wrap gap-3">
				<Link className="rounded-md border px-4 py-2" href="/docs">
					Read the docs
				</Link>
				<Link
					className="rounded-md border px-4 py-2"
					href="/docs/generated/catalog"
				>
					Browse catalog
				</Link>
				<Link className="rounded-md border px-4 py-2" href="/llms.txt">
					LLM index
				</Link>
			</nav>
		</main>
	);
}
