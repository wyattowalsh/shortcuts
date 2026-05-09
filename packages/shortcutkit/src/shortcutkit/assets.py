import hashlib
from pathlib import Path
from typing import Any

from shortcutkit.models import ShortcutManifest


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_relative_path(root: Path, value: str | None) -> Path | None:
    if not value:
        return None
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    resolved_root = root.resolve()
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError:
        return None
    return resolved


def icon_metadata(root: Path, manifest: ShortcutManifest) -> dict[str, Any] | None:
    icon = manifest.icon or {}
    if not isinstance(icon, dict):
        return None
    path = package_relative_path(root, icon.get("path"))
    if path is None or not path.exists() or not path.is_file():
        return None
    relative = path.relative_to(root)
    docs_path = f"/catalog-icons/{manifest.id}{path.suffix.lower()}"
    return {
        "path": str(relative),
        "sha256": sha256_file(path),
        "bytes": path.stat().st_size,
        "alt": icon.get("alt") or f"{manifest.name} icon",
        "docs_path": docs_path,
    }
