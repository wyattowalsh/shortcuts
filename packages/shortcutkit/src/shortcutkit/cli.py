import json
import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from shortcutkit import __version__
from shortcutkit.adapters import adapter_infos, adapters_json, build_package
from shortcutkit.catalog import catalog_file, discover_manifests, render_catalog
from shortcutkit.docs import generated_reference, sync_catalog_icon_assets
from shortcutkit.html_runtime import HtmlRuntimeError, analyze_html, bundle_html, publish_html
from shortcutkit.linting import lint_package
from shortcutkit.manifest import ManifestError, load_manifest
from shortcutkit.paths import find_repo_root
from shortcutkit.release import release_metadata, release_metadata_json, release_notes
from shortcutkit.runtime import runtime_result_json, runtime_test_package
from shortcutkit.security import audit_json, audit_package

app = typer.Typer(help="Developer tooling for source-first Apple Shortcuts projects.")
catalog_app = typer.Typer(help="Catalog commands.")
security_app = typer.Typer(help="Security review commands.")
docs_app = typer.Typer(help="Documentation generation commands.")
adapter_app = typer.Typer(help="Adapter capability commands.")
release_app = typer.Typer(help="Release metadata commands.")
html_app = typer.Typer(help="HTML runtime commands.")
console = Console()
error_console = Console(stderr=True)
DEFAULT_DOCS_ROOT = Path("apps/docs")


def _stdout(text: str) -> None:
    sys.stdout.write(text)


def version_callback(value: bool) -> None:
    if value:
        console.print(__version__)
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False, "--version", callback=version_callback, help="Print shortcutkit version."
    ),
) -> None:
    _ = version


@app.command()
def validate(path: Path) -> None:
    try:
        manifest = load_manifest(path)
    except (FileNotFoundError, ManifestError) as exc:
        console.print(f"[red]validation failed:[/] {exc}")
        raise typer.Exit(1) from exc
    console.print(f"[green]valid[/] {manifest.id} {manifest.version}")


@app.command()
def lint(path: Path) -> None:
    try:
        issues = lint_package(path)
    except (FileNotFoundError, ManifestError) as exc:
        console.print(f"[red]lint failed:[/] {exc}")
        raise typer.Exit(1) from exc
    if issues:
        for issue in issues:
            console.print(f"[red]issue:[/] {issue}")
        raise typer.Exit(1)
    console.print("[green]lint passed[/]")


def _validate_and_lint_quiet(path: Path, *, command: str) -> None:
    try:
        issues = lint_package(path)
    except (FileNotFoundError, ManifestError) as exc:
        error_console.print(f"[red]{command} failed:[/] {exc}")
        raise typer.Exit(1) from exc
    if issues:
        for issue in issues:
            error_console.print(f"[red]issue:[/] {issue}")
        raise typer.Exit(1)


@catalog_app.command("generate")
def catalog_generate(
    check: bool = typer.Option(False, "--check", help="Fail if catalog/shortcuts.json is stale."),
) -> None:
    root = find_repo_root()
    output = render_catalog(root)
    target = catalog_file(root)
    if check:
        if not target.exists() or target.read_text(encoding="utf-8") != output:
            console.print(f"[red]catalog drift:[/] {target}")
            raise typer.Exit(1)
        console.print("[green]catalog up to date[/]")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(output, encoding="utf-8")
    console.print(f"[green]wrote[/] {target}")


@security_app.command("audit")
def security_audit(
    path: Annotated[Path | None, typer.Argument()] = None,
    strict: bool = typer.Option(
        False, "--strict", help="Fail closed for unknown high-risk findings."
    ),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON audit output."),
) -> None:
    targets = (
        [path]
        if path is not None
        else [item.parent for item in discover_manifests(find_repo_root())]
    )
    audits = []
    try:
        audits = [audit_package(target, strict=strict) for target in targets]
    except (FileNotFoundError, ManifestError) as exc:
        console.print(f"[red]audit failed:[/] {exc}")
        raise typer.Exit(1) from exc
    if json_output:
        if len(audits) == 1:
            _stdout(audit_json(audits[0]))
        else:
            _stdout(
                json.dumps([audit.model_dump() for audit in audits], indent=2, sort_keys=True)
                + "\n"
            )
    else:
        for audit in audits:
            status = "passed" if audit.passed else "failed"
            console.print(f"security audit {status}: {audit.package_id}")
            for finding in audit.findings:
                console.print(
                    f"- {finding.severity} {finding.status} {finding.id}: {finding.detail}"
                )
    if any(not audit.passed for audit in audits):
        raise typer.Exit(1)


@docs_app.command("generate")
def docs_generate(
    docs_root: Annotated[Path, typer.Option("--docs-root")] = DEFAULT_DOCS_ROOT,
    check: bool = typer.Option(False, "--check", help="Fail if generated reference is stale."),
) -> None:
    target = docs_root / "content" / "docs" / "generated" / "catalog.mdx"
    output = generated_reference()
    if check:
        stale_icons = sync_catalog_icon_assets(docs_root, check=True)
        if not target.exists() or target.read_text(encoding="utf-8") != output:
            console.print(f"[red]generated docs drift:[/] {target}")
            raise typer.Exit(1)
        if stale_icons:
            console.print(f"[red]generated icon drift:[/] {stale_icons[0]}")
            raise typer.Exit(1)
        console.print("[green]generated docs up to date[/]")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(output, encoding="utf-8")
    sync_catalog_icon_assets(docs_root)
    console.print(f"[green]wrote[/] {target}")


@adapter_app.command("check")
def adapter_check(
    json_output: bool = typer.Option(False, "--json", help="Emit JSON output."),
) -> None:
    if json_output:
        _stdout(adapters_json())
        return
    console.print("adapter capability matrix")
    for adapter in adapter_infos():
        status = "available" if adapter.available else "missing"
        console.print(f"- {adapter.id}: {status}; {adapter.notes}")


@app.command()
def build(
    path: Path,
    run_external: bool = typer.Option(
        False, "--run-external", help="Run external compiler adapters."
    ),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON build metadata."),
) -> None:
    if json_output:
        _validate_and_lint_quiet(path, command="build")
    else:
        validate(path)
        lint(path)
    result = build_package(path, run_external=run_external)
    if json_output:
        _stdout(result.model_dump_json(indent=2) + "\n")
    else:
        console.print(f"build {result.status}: {result.message}")
    if result.status == "unavailable":
        raise typer.Exit(1)


@app.command()
def test(
    path: Path,
    run: bool = typer.Option(False, "--run", help="Run optional macOS runtime tests."),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON runtime result."),
) -> None:
    if json_output:
        _validate_and_lint_quiet(path, command="test")
    else:
        validate(path)
        lint(path)
    result = runtime_test_package(path, run=run)
    if json_output:
        _stdout(runtime_result_json(result))
    else:
        console.print(f"runtime test {result.status}: {result.message}")
    if result.status == "failed":
        raise typer.Exit(1)


@release_app.command("metadata")
def release_metadata_command(path: Path) -> None:
    _stdout(release_metadata_json(release_metadata(path)))


@release_app.command("notes")
def release_notes_command(
    path: Path,
    output: Annotated[Path | None, typer.Option("--output")] = None,
) -> None:
    rendered = release_notes(path)
    if output is None:
        _stdout(rendered + "\n")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    console.print(f"[green]wrote[/] {output}")


@html_app.command("analyze")
def html_analyze(
    entrypoint: Path,
    json_output: bool = typer.Option(False, "--json", help="Emit JSON analysis output."),
) -> None:
    try:
        analysis = analyze_html(entrypoint)
    except HtmlRuntimeError as exc:
        console.print(f"[red]html analyze failed:[/] {exc}")
        raise typer.Exit(1) from exc
    if json_output:
        _stdout(analysis.model_dump_json(indent=2) + "\n")
        return
    console.print(f"HTML local-bundled profile: {analysis.status}")
    console.print(f"Size gate: {analysis.size_gate}; raw bytes: {analysis.raw_bytes}")
    for diagnostic in analysis.diagnostics:
        console.print(f"- {diagnostic.severity} {diagnostic.id}: {diagnostic.detail}")
    if analysis.status == "unsupported":
        raise typer.Exit(1)


@html_app.command("bundle")
def html_bundle(
    entrypoint: Path,
    output: Annotated[Path, typer.Option("--output")],
    json_output: bool = typer.Option(False, "--json", help="Emit JSON bundle output."),
) -> None:
    try:
        result = bundle_html(entrypoint, output)
    except HtmlRuntimeError as exc:
        console.print(f"[red]html bundle failed:[/] {exc}")
        raise typer.Exit(1) from exc
    if json_output:
        _stdout(result.model_dump_json(indent=2) + "\n")
    else:
        console.print(f"html bundle {result.status}: {result.message}")
    if result.status == "failed":
        raise typer.Exit(1)


@html_app.command("publish")
def html_publish(
    site: Path,
    provider: str = typer.Option("here-now", "--provider", help="Static host provider."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Plan publish without network egress."),
    run: bool = typer.Option(False, "--run", help="Attempt a real provider publish."),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON publish output."),
) -> None:
    _ = dry_run
    try:
        result = publish_html(site, provider=provider, run=run)
    except HtmlRuntimeError as exc:
        console.print(f"[red]html publish failed:[/] {exc}")
        raise typer.Exit(1) from exc
    if json_output:
        _stdout(result.model_dump_json(indent=2) + "\n")
    else:
        console.print(f"html publish {result.status}: {result.message}")
    if result.status == "blocked":
        raise typer.Exit(1)


app.add_typer(catalog_app, name="catalog")
app.add_typer(security_app, name="security")
app.add_typer(docs_app, name="docs")
app.add_typer(adapter_app, name="adapter")
app.add_typer(release_app, name="release")
app.add_typer(html_app, name="html")
