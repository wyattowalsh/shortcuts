from pathlib import Path

import shortcutkit.adapters as shortcutkit_adapters
import shortcutkit.manifest as shortcutkit_manifest
import shortcutkit.security as shortcutkit_security
from shortcutkit.adapters import adapter_infos, build_package
from shortcutkit.models import AdapterCapabilities, AdapterInfo
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


def test_cherri_build_writes_dist_artifact_and_cleans_unsigned_sidecar(
    tmp_path: Path, monkeypatch
) -> None:
    package = tmp_path / "shortcut"
    source = package / "src" / "test.cherri"
    source.parent.mkdir(parents=True)
    source.write_text("#define name Test Cherri\n", encoding="utf-8")
    (package / "shortcut.yml").write_text(
        """
id: com.shortcuts.tests.cherri
name: Test Cherri
version: 0.1.0
summary: Fixture for external Cherri adapter behavior.
category: testing
status: experimental
license: MIT
maintainers:
  - name: test maintainer
source:
  mode: cherri
  entrypoint: src/test.cherri
declared_permissions:
  clipboard:
    read: false
    write: false
  network:
    allowed: false
    domains: []
  ai:
    uses_model_action: false
  shell: false
  url_schemes: []
security:
  tier: low
  data_leaves_device: false
  review_status: fixture
tests:
  static:
    enabled: true
  runtime:
    enabled: false
  manual:
    - Fixture-only manual verification placeholder.
""".lstrip(),
        encoding="utf-8",
    )
    captured: dict[str, object] = {}

    def fake_adapter_infos() -> list[AdapterInfo]:
        return [
            AdapterInfo(
                id="cherri",
                name="Fake Cherri",
                binary="cherri",
                available=True,
                capabilities=AdapterCapabilities(
                    build=True, export=True, inspect=False, test=False, license="external"
                ),
                notes="Runs a fake Cherri binary for adapter tests.",
            )
        ]

    def fake_run(command: list[str], cwd: Path, check: bool) -> None:
        captured["command"] = command
        captured["cwd"] = cwd
        captured["check"] = check
        output = next(
            item.removeprefix("--output=") for item in command if item.startswith("--output=")
        )
        Path(output).write_bytes(b"shortcut")
        (source.parent / "Test Cherri_unsigned.shortcut").write_bytes(b"unsigned")

    monkeypatch.setattr(shortcutkit_adapters, "adapter_infos", fake_adapter_infos)
    monkeypatch.setattr(shortcutkit_adapters.subprocess, "run", fake_run)
    monkeypatch.setattr(
        shortcutkit_manifest,
        "find_repo_root",
        lambda _path: Path(__file__).resolve().parents[3],
    )

    result = build_package(package, run_external=True)

    assert result.status == "built"
    assert result.artifact_path == "dist/Test Cherri.shortcut"
    assert (package / result.artifact_path).read_bytes() == b"shortcut"
    assert not (source.parent / "Test Cherri_unsigned.shortcut").exists()
    assert captured["cwd"] == package
    assert captured["check"] is True
    command = captured["command"]
    assert isinstance(command, list)
    assert "--derive-uuids" in command
    assert f"--output={package / result.artifact_path}" in command


def test_cherri_dry_run_does_not_create_dist(tmp_path: Path, monkeypatch) -> None:
    package = tmp_path / "shortcut"
    source = package / "src" / "test.cherri"
    source.parent.mkdir(parents=True)
    source.write_text("#define name Test Cherri\n", encoding="utf-8")
    (package / "shortcut.yml").write_text(
        """
id: com.shortcuts.tests.cherri.dry-run
name: Test Cherri Dry Run
version: 0.1.0
summary: Fixture for dry-run Cherri adapter behavior.
category: testing
status: experimental
license: MIT
maintainers:
  - name: test maintainer
source:
  mode: cherri
  entrypoint: src/test.cherri
declared_permissions:
  clipboard:
    read: false
    write: false
  network:
    allowed: false
    domains: []
  ai:
    uses_model_action: false
  shell: false
  url_schemes: []
security:
  tier: low
  data_leaves_device: false
  review_status: fixture
tests:
  static:
    enabled: true
  runtime:
    enabled: false
  manual:
    - Fixture-only manual verification placeholder.
""".lstrip(),
        encoding="utf-8",
    )

    def fake_adapter_infos() -> list[AdapterInfo]:
        return [
            AdapterInfo(
                id="cherri",
                name="Fake Cherri",
                binary="cherri",
                available=True,
                capabilities=AdapterCapabilities(
                    build=True, export=True, inspect=False, test=False, license="external"
                ),
                notes="Runs a fake Cherri binary for adapter tests.",
            )
        ]

    monkeypatch.setattr(shortcutkit_adapters, "adapter_infos", fake_adapter_infos)
    monkeypatch.setattr(
        shortcutkit_manifest,
        "find_repo_root",
        lambda _path: Path(__file__).resolve().parents[3],
    )

    result = build_package(package, run_external=False)

    assert result.status == "skipped"
    assert not (package / "dist").exists()


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


def test_release_metadata_and_notes_include_declared_icon() -> None:
    root = Path(__file__).resolve().parents[3]
    package = root / "shortcuts" / "open-html-in-safari"
    metadata = release_metadata(package)
    notes = release_notes(package)
    icon_sha256 = "4413115dfe470147c8240fa8e0231469032adb24f579db2e708e218b65fdd702"
    icon_alt = "Open HTML shortcut icon with an HTML document, Safari compass, and share arrow."

    assert metadata.assets == [
        {
            "kind": "icon",
            "path": "icon.png",
            "sha256": icon_sha256,
            "bytes": (package / "icon.png").stat().st_size,
            "alt": icon_alt,
            "docs_path": "/catalog-icons/com.shortcuts.open-html-in-safari.png",
        }
    ]
    assert f"`icon.png` (icon) SHA-256 `{icon_sha256}`" in notes


def test_release_metadata_includes_bundled_html_asset(tmp_path: Path, monkeypatch) -> None:
    package = tmp_path / "shortcut"
    dist = package / "dist"
    dist.mkdir(parents=True)
    (package / "README.md").write_text("# Fixture\n", encoding="utf-8")
    bundle = dist / "Fixture.bundled.html"
    bundle.write_text("<!doctype html><title>Fixture</title>", encoding="utf-8")
    (package / "shortcut.yml").write_text(
        """
id: com.shortcuts.tests.html-runtime-release
name: HTML Runtime Release Fixture
version: 0.1.0
summary: Fixture for bundled HTML release metadata.
category: testing
status: experimental
license: MIT
maintainers:
  - name: test maintainer
source:
  mode: manual
  entrypoint: src/shortcut.md
declared_permissions:
  clipboard:
    read: false
    write: false
  network:
    allowed: false
    domains: []
  ai:
    uses_model_action: false
  shell: false
  url_schemes:
    - data
html_runtime:
  profiles:
    - id: local-bundled
      support: constrained
      output: dist/Fixture.bundled.html
security:
  tier: low
  data_leaves_device: false
  review_status: fixture
tests:
  static:
    enabled: true
  runtime:
    enabled: false
  manual:
    - Fixture-only manual verification placeholder.
""".lstrip(),
        encoding="utf-8",
    )
    (package / "src").mkdir()
    (package / "src" / "shortcut.md").write_text("Open data:text/html;base64,abc", encoding="utf-8")
    monkeypatch.setattr(
        shortcutkit_manifest,
        "find_repo_root",
        lambda _path: Path(__file__).resolve().parents[3],
    )
    monkeypatch.setattr(
        shortcutkit_security,
        "find_repo_root",
        lambda _path: Path(__file__).resolve().parents[3],
    )

    metadata = release_metadata(package)

    assert any(
        asset["kind"] == "html-runtime" and asset["path"] == "dist/Fixture.bundled.html"
        for asset in metadata.assets
    )
