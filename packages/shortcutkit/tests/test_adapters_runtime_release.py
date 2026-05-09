from pathlib import Path

from shortcutkit.adapters import adapter_infos, build_package
from shortcutkit.release import release_metadata, release_notes
from shortcutkit.runtime import runtime_test_package


def test_adapter_matrix_includes_external_boundaries() -> None:
    adapters = {adapter.id: adapter for adapter in adapter_infos()}
    assert adapters["manual"].available is True
    assert adapters["cherri"].capabilities.license == "external"
    assert adapters["jelly"].capabilities.license == "external"


def test_manual_build_returns_source_hash_metadata() -> None:
    root = Path(__file__).resolve().parents[3]
    result = build_package(root / "shortcuts" / "examples" / "clean-clipboard")
    assert result.package_id == "com.shortcuts.examples.clean-clipboard"
    assert result.status == "manual"
    assert len(result.source_hash) == 64


def test_build_rejects_entrypoint_traversal() -> None:
    fixture = Path(__file__).parent / "fixtures" / "traversal-entrypoint"
    result = build_package(fixture)
    assert result.status == "unavailable"
    assert "inside the package" in result.message


def test_runtime_disabled_by_default() -> None:
    root = Path(__file__).resolve().parents[3]
    result = runtime_test_package(root / "shortcuts" / "examples" / "clean-clipboard")
    assert result.status == "disabled"


def test_release_metadata_and_notes_include_audit_summary() -> None:
    root = Path(__file__).resolve().parents[3]
    package = root / "shortcuts" / "examples" / "clean-clipboard"
    metadata = release_metadata(package)
    notes = release_notes(package)
    assert metadata.package_id == "com.shortcuts.examples.clean-clipboard"
    assert metadata.audit.actiondb_version == "0.1.0"
    assert "Permission badges" in notes
