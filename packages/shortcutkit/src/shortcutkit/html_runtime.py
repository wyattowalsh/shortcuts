import hashlib
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Literal, cast
from urllib.parse import urlparse

from shortcutkit.assets import sha256_file
from shortcutkit.models import (
    HtmlRuntimeAnalysis,
    HtmlRuntimeAsset,
    HtmlRuntimeBundleResult,
    HtmlRuntimeDiagnostic,
    HtmlRuntimePublishFile,
    HtmlRuntimePublishResult,
)

GREEN_SIZE_LIMIT = 500 * 1024
YELLOW_SIZE_LIMIT = 2 * 1024 * 1024
SUPPORTED_INLINE_SUFFIXES = {".css", ".js", ".mjs"}
FORBIDDEN_SUFFIXES = {
    ".map",
    ".wasm",
    ".mp4",
    ".mov",
    ".webm",
    ".mp3",
    ".m4a",
    ".wav",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
}


class HtmlRuntimeError(ValueError):
    pass


class _ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.inline_candidates: list[tuple[str, str, str]] = []
        self.references: list[tuple[str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key.lower(): value or "" for key, value in attrs}
        tag_name = tag.lower()
        if tag_name == "script" and attributes.get("src"):
            src = attributes["src"]
            self.inline_candidates.append(("javascript", src, tag_name))
            self.references.append(("javascript", src, tag_name))
            return
        if tag_name == "link" and attributes.get("href"):
            href = attributes["href"]
            rel = {part.strip().lower() for part in attributes.get("rel", "").split()}
            kind = "css" if "stylesheet" in rel else "file"
            if kind == "css":
                self.inline_candidates.append((kind, href, tag_name))
            self.references.append((kind, href, tag_name))
            return
        for attr_name in ("src", "href"):
            if attributes.get(attr_name):
                self.references.append(("file", attributes[attr_name], tag_name))


def _is_external_reference(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https", "//"} or value.startswith("//")


def _is_inline_reference(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"data", "mailto", "tel", "#"} or value.startswith("#")


def _size_gate(size: int) -> Literal["green", "yellow", "red"]:
    if size <= GREEN_SIZE_LIMIT:
        return "green"
    if size <= YELLOW_SIZE_LIMIT:
        return "yellow"
    return "red"


def _asset_path(entrypoint: Path, source: str) -> Path | None:
    parsed = urlparse(source)
    if parsed.scheme or source.startswith("/"):
        return None
    path = Path(parsed.path)
    if path.is_absolute() or ".." in path.parts:
        return None
    resolved_root = entrypoint.parent.resolve()
    resolved = (entrypoint.parent / path).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError:
        return None
    return resolved


def _diagnostic(
    diagnostic_id: str,
    severity: Literal["info", "warning", "error"],
    detail: str,
    path: str | None = None,
) -> HtmlRuntimeDiagnostic:
    return HtmlRuntimeDiagnostic(
        id=diagnostic_id,
        severity=severity,
        detail=detail,
        path=path,
    )


def analyze_html(entrypoint: Path) -> HtmlRuntimeAnalysis:
    if not entrypoint.exists() or not entrypoint.is_file():
        raise HtmlRuntimeError(f"HTML entrypoint does not exist: {entrypoint}")
    html = entrypoint.read_text(encoding="utf-8", errors="ignore")
    parser = _ReferenceParser()
    parser.feed(html)

    raw_bytes = entrypoint.stat().st_size
    gate = _size_gate(raw_bytes)
    assets_by_path: dict[Path, HtmlRuntimeAsset] = {}
    diagnostics: list[HtmlRuntimeDiagnostic] = []
    if gate == "yellow":
        diagnostics.append(
            _diagnostic(
                "warning.size.yellow",
                "warning",
                "Bundled HTML is larger than 500KB raw and may be slow in Shortcuts.",
                str(entrypoint),
            )
        )
    elif gate == "red":
        diagnostics.append(
            _diagnostic(
                "unsupported.size.red",
                "error",
                "Bundled HTML is larger than 2MB raw and is not supported for local profile.",
                str(entrypoint),
            )
        )

    inline_sources = {source for _, source, _ in parser.inline_candidates}
    for kind, source, tag_name in parser.references:
        if _is_inline_reference(source):
            continue
        if _is_external_reference(source):
            diagnostics.append(
                _diagnostic(
                    "unsupported.external-reference",
                    "error",
                    f"External {tag_name} reference cannot be bundled locally: {source}",
                    source,
                )
            )
            continue
        asset = _asset_path(entrypoint, source)
        if asset is None:
            diagnostics.append(
                _diagnostic(
                    "unsupported.path-reference",
                    "error",
                    f"Reference must stay inside the HTML entrypoint folder: {source}",
                    source,
                )
            )
            continue
        suffix = asset.suffix.lower()
        if suffix in FORBIDDEN_SUFFIXES:
            diagnostics.append(
                _diagnostic(
                    "unsupported.asset-type",
                    "error",
                    f"Local bundled profile does not support {suffix} assets: {source}",
                    source,
                )
            )
            continue
        if source in inline_sources and suffix not in SUPPORTED_INLINE_SUFFIXES:
            diagnostics.append(
                _diagnostic(
                    "unsupported.inline-type",
                    "error",
                    f"Only CSS and JavaScript can be inlined, got: {source}",
                    source,
                )
            )
            continue
        if not asset.exists() or not asset.is_file():
            diagnostics.append(
                _diagnostic(
                    "unsupported.missing-asset",
                    "error",
                    f"Referenced asset is missing: {source}",
                    source,
                )
            )
            continue
        if source in inline_sources:
            assets_by_path[asset] = HtmlRuntimeAsset(
                path=str(asset),
                kind=cast(Literal["css", "javascript", "file"], kind)
                if kind in {"css", "javascript"}
                else "file",
                bytes=asset.stat().st_size,
                sha256=sha256_file(asset),
                source=source,
            )

    if any(diagnostic.severity == "error" for diagnostic in diagnostics):
        status = "unsupported"
    elif any(diagnostic.severity == "warning" for diagnostic in diagnostics):
        status = "warning"
    else:
        status = "supported"
    return HtmlRuntimeAnalysis(
        entrypoint=str(entrypoint),
        profile="local-bundled",
        status=status,
        raw_bytes=raw_bytes,
        size_gate=gate,
        assets=[assets_by_path[path] for path in sorted(assets_by_path)],
        diagnostics=diagnostics,
    )


def _replace_stylesheet(html: str, source: str, content: str) -> str:
    pattern = re.compile(
        rf"<link\b(?=[^>]*\bhref=(['\"]){re.escape(source)}\1)"
        rf"(?=[^>]*\brel=(['\"])[^'\"]*stylesheet[^'\"]*\2)[^>]*>",
        re.IGNORECASE,
    )
    return pattern.sub(f"<style>\n{content}\n</style>", html)


def _replace_script(html: str, source: str, content: str) -> str:
    pattern = re.compile(
        rf"<script\b(?=[^>]*\bsrc=(['\"]){re.escape(source)}\1)[^>]*>\s*</script>",
        re.IGNORECASE,
    )
    return pattern.sub(f"<script>\n{content}\n</script>", html)


def bundle_html(entrypoint: Path, output: Path) -> HtmlRuntimeBundleResult:
    analysis = analyze_html(entrypoint)
    if analysis.status == "unsupported":
        return HtmlRuntimeBundleResult(
            entrypoint=str(entrypoint),
            output_path=str(output),
            status="failed",
            message="HTML entrypoint is not supported by the local bundled profile.",
            analysis=analysis,
        )

    html = entrypoint.read_text(encoding="utf-8")
    for asset in analysis.assets:
        if asset.source is None:
            continue
        content = Path(asset.path).read_text(encoding="utf-8")
        if asset.kind == "css":
            html = _replace_stylesheet(html, asset.source, content)
        elif asset.kind == "javascript":
            html = _replace_script(html, asset.source, content)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    return HtmlRuntimeBundleResult(
        entrypoint=str(entrypoint),
        output_path=str(output),
        status="bundled",
        message="Wrote bundled HTML for the local Shortcuts data URL profile.",
        bytes=output.stat().st_size,
        sha256=sha256_file(output),
        analysis=analysis,
    )


def publish_html(site: Path, *, provider: str, run: bool) -> HtmlRuntimePublishResult:
    if provider != "here-now":
        raise HtmlRuntimeError(f"Unsupported HTML hosting provider: {provider}")
    if not site.exists():
        raise HtmlRuntimeError(f"HTML site path does not exist: {site}")
    files = [site] if site.is_file() else sorted(path for path in site.rglob("*") if path.is_file())
    root = site.parent if site.is_file() else site
    publish_files = [
        HtmlRuntimePublishFile(
            path=str(path.relative_to(root)),
            bytes=path.stat().st_size,
            sha256=sha256_file(path),
        )
        for path in files
    ]
    if run:
        return HtmlRuntimePublishResult(
            provider="here-now",
            site=str(site),
            status="blocked",
            dry_run=False,
            files=publish_files,
            message=(
                "Real here.now publish is intentionally gated until credentials/API details "
                "and data-egress approval are provided. Re-run with --dry-run for planning."
            ),
        )
    fingerprint = hashlib.sha256(
        "\n".join(file.sha256 for file in publish_files).encode("utf-8")
    ).hexdigest()
    return HtmlRuntimePublishResult(
        provider="here-now",
        site=str(site),
        status="dry-run",
        dry_run=True,
        files=publish_files,
        message=f"Dry run only; no network publish occurred. Site fingerprint {fingerprint}.",
    )
