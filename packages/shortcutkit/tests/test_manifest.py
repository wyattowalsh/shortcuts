from pathlib import Path

import pytest
from shortcutkit.manifest import ManifestError, load_manifest


def test_clean_clipboard_manifest_loads() -> None:
    root = Path(__file__).resolve().parents[3]
    manifest = load_manifest(root / "shortcuts" / "examples" / "clean-clipboard")
    assert manifest.id == "com.shortcuts.examples.clean-clipboard"
    assert manifest.declared_permissions["clipboard"]["read"] is True


def test_invalid_manifest_reports_path_aware_error() -> None:
    fixture = Path(__file__).parent / "fixtures" / "invalid-manifest"
    with pytest.raises(ManifestError, match="version"):
        load_manifest(fixture)
