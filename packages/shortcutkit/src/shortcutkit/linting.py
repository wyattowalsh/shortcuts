from pathlib import Path

from shortcutkit.assets import package_relative_path
from shortcutkit.manifest import load_manifest
from shortcutkit.paths import package_root


def lint_package(path: Path) -> list[str]:
    root = package_root(path)
    manifest = load_manifest(root)
    issues: list[str] = []

    readme = root / "README.md"
    if not readme.exists():
        issues.append(f"{root}: missing README.md")
    else:
        text = readme.read_text(encoding="utf-8")
        if manifest.name not in text and manifest.summary not in text:
            issues.append(f"{readme}: must mention the shortcut name or summary")

    for artifact in root.rglob("*.shortcut"):
        if "dist" not in artifact.relative_to(root).parts:
            issues.append(f"{artifact}: .shortcut artifacts must live under dist/")

    icon = manifest.icon or {}
    if isinstance(icon, dict) and icon.get("path"):
        icon_path = package_relative_path(root, icon.get("path"))
        if icon_path is None or not icon_path.is_file():
            issues.append(f"{root}: declared icon is missing or outside the package")

    return issues
