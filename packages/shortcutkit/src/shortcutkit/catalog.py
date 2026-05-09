import json
from pathlib import Path
from typing import Any, TypedDict

from shortcutkit.assets import icon_metadata
from shortcutkit.manifest import load_manifest
from shortcutkit.paths import find_repo_root
from shortcutkit.security import audit_package


class CatalogEntry(TypedDict):
    id: str
    name: str
    version: str
    summary: str
    category: str
    status: str
    path: str
    security_tier: str
    permission_badges: list[str]
    icon: dict[str, Any] | None
    audit_passed: bool
    domains: list[str]
    review_required: bool
    html_runtime: dict[str, Any] | None


class CatalogPayload(TypedDict):
    version: int
    shortcuts: list[CatalogEntry]


def discover_manifests(root: Path) -> list[Path]:
    shortcuts_root = root / "shortcuts"
    return sorted(shortcuts_root.glob("**/shortcut.yml"))


def catalog_payload(root: Path) -> CatalogPayload:
    entries: list[CatalogEntry] = []
    for manifest_path in discover_manifests(root):
        package = manifest_path.parent
        manifest = load_manifest(package)
        audit = audit_package(package, strict=True)
        summary: dict[str, Any] = audit.summary
        entries.append(
            {
                "id": manifest.id,
                "name": manifest.name,
                "version": manifest.version,
                "summary": manifest.summary,
                "category": manifest.category,
                "status": manifest.status,
                "path": str(package.relative_to(root)),
                "security_tier": (manifest.security or {}).get("tier", "unknown"),
                "permission_badges": list(summary.get("badges", [])),
                "icon": icon_metadata(package, manifest),
                "audit_passed": audit.passed,
                "domains": list(summary.get("domains", [])),
                "review_required": bool(summary.get("review_required", False)),
                "html_runtime": manifest.html_runtime,
            }
        )
    return {"version": 1, "shortcuts": entries}


def render_catalog(root: Path | None = None) -> str:
    payload = catalog_payload(root or find_repo_root())
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def catalog_file(root: Path | None = None) -> Path:
    return (root or find_repo_root()) / "catalog" / "catalog.json"
