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


def test_runtime_disabled_manifest_requires_manual_steps() -> None:
    fixture = Path(__file__).parent / "fixtures" / "missing-manual-tests"
    with pytest.raises(ManifestError, match="manual"):
        load_manifest(fixture)


def test_manifest_without_runtime_requires_manual_steps() -> None:
    fixture = Path(__file__).parent / "fixtures" / "missing-runtime-tests"
    with pytest.raises(ManifestError, match="manual"):
        load_manifest(fixture)


def test_manifest_rejects_blank_manual_steps() -> None:
    fixture = Path(__file__).parent / "fixtures" / "blank-manual-tests"
    with pytest.raises(ManifestError, match="manual"):
        load_manifest(fixture)


def test_open_html_manifest_declares_runtime_profiles() -> None:
    root = Path(__file__).resolve().parents[3]
    manifest = load_manifest(root / "shortcuts" / "open-html-in-safari")
    assert manifest.html_runtime is not None
    profiles = {profile["id"]: profile for profile in manifest.html_runtime["profiles"]}
    assert profiles["local-bundled"]["support"] == "constrained"
    assert profiles["hosted"]["provider"] == "here-now"
