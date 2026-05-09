import json
from pathlib import Path
from typing import Any, TypedDict

from shortcutkit.manifest import load_manifest
from shortcutkit.paths import find_repo_root
from shortcutkit.security import audit_package, permission_badges


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
    audit_passed: bool
    domains: list[str]
    review_required: bool


class CatalogPayload(TypedDict):
    version: int
    shortcuts: list[CatalogEntry]


def discover_manifests(root: Path) -> list[Path]:
    return sorted((root / "shortcuts" / "examples").glob("*/shortcut.yml"))


def catalog_payload(root: Path) -> CatalogPayload:
    entries: list[CatalogEntry] = []
    for manifest_path in discover_manifests(root):
        package = manifest_path.parent
        manifest = load_manifest(package)
        audit = audit_package(package, strict=False)
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
                "permission_badges": permission_badges(audit),
                "audit_passed": audit.passed,
                "domains": list(summary.get("domains", [])),
                "review_required": bool(summary.get("review_required", False)),
            }
        )
    return {"version": 1, "shortcuts": entries}


def render_catalog(root: Path | None = None) -> str:
    payload = catalog_payload(root or find_repo_root())
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def catalog_file(root: Path | None = None) -> Path:
    return (root or find_repo_root()) / "catalog" / "catalog.json"
