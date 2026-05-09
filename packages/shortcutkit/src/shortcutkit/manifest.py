import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from shortcutkit.models import ShortcutManifest
from shortcutkit.paths import find_repo_root, package_root


class ManifestError(ValueError):
    pass


def manifest_path(path: Path) -> Path:
    return package_root(path) / "shortcut.yml"


def load_manifest_data(path: Path) -> dict[str, Any]:
    target = manifest_path(path)
    try:
        payload = yaml.safe_load(target.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ManifestError(f"{target}: invalid YAML: {exc}") from exc
    if not isinstance(payload, dict):
        raise ManifestError(f"{target}: expected a YAML mapping")
    return payload


def load_manifest(path: Path) -> ShortcutManifest:
    data = load_manifest_data(path)
    root = find_repo_root(path)
    schema_path = root / "packages" / "schemas" / "shortcut-manifest.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "<root>"
        raise ManifestError(f"{manifest_path(path)}:{location}: {first.message}")
    try:
        return ShortcutManifest.model_validate(data)
    except ValidationError as exc:
        raise ManifestError(f"{manifest_path(path)}: {exc}") from exc
