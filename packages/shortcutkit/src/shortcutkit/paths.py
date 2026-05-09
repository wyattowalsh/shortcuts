from pathlib import Path


def find_repo_root(start: Path | None = None) -> Path:
    cursor = (start or Path.cwd()).resolve()
    for candidate in [cursor, *cursor.parents]:
        if (candidate / "packages" / "schemas" / "shortcut-manifest.schema.json").exists():
            return candidate
    raise RuntimeError("Could not find repository root containing packages/schemas")


def package_root(path: Path) -> Path:
    candidate = path.resolve()
    if candidate.is_file():
        candidate = candidate.parent
    manifest = candidate / "shortcut.yml"
    if manifest.exists():
        return candidate
    if candidate.name == "shortcut.yml" and candidate.exists():
        return candidate.parent
    raise FileNotFoundError(f"No shortcut.yml found at {candidate}")
