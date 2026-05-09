from pathlib import Path

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

    return issues
