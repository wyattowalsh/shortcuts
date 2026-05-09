import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from shortcutkit import __version__
from shortcutkit.adapters import adapter_infos, adapters_json, build_package
from shortcutkit.catalog import catalog_file, discover_manifests, render_catalog
from shortcutkit.docs import generated_reference
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
console = Console()
DEFAULT_DOCS_ROOT = Path("apps/docs")


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
    path: Path | None = None,
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
            console.print(audit_json(audits[0]), end="")
        else:
            console.print(
                json.dumps([audit.model_dump() for audit in audits], indent=2, sort_keys=True)
                + "\n",
                end="",
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
        if not target.exists() or target.read_text(encoding="utf-8") != output:
            console.print(f"[red]generated docs drift:[/] {target}")
            raise typer.Exit(1)
        console.print("[green]generated docs up to date[/]")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(output, encoding="utf-8")
    console.print(f"[green]wrote[/] {target}")


@adapter_app.command("check")
def adapter_check(
    json_output: bool = typer.Option(False, "--json", help="Emit JSON output."),
) -> None:
    if json_output:
        console.print(adapters_json(), end="")
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
    validate(path)
    lint(path)
    result = build_package(path, run_external=run_external)
    if json_output:
        console.print(result.model_dump_json(indent=2), end="\n")
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
    validate(path)
    result = runtime_test_package(path, run=run)
    if json_output:
        console.print(runtime_result_json(result), end="")
    else:
        console.print(f"runtime test {result.status}: {result.message}")
    if result.status == "failed":
        raise typer.Exit(1)


@release_app.command("metadata")
def release_metadata_command(path: Path) -> None:
    console.print(release_metadata_json(release_metadata(path)), end="")


@release_app.command("notes")
def release_notes_command(
    path: Path,
    output: Annotated[Path | None, typer.Option("--output")] = None,
) -> None:
    rendered = release_notes(path)
    if output is None:
        console.print(rendered)
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    console.print(f"[green]wrote[/] {output}")


app.add_typer(catalog_app, name="catalog")
app.add_typer(security_app, name="security")
app.add_typer(docs_app, name="docs")
app.add_typer(adapter_app, name="adapter")
app.add_typer(release_app, name="release")
