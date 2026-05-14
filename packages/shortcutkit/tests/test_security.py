from pathlib import Path

from shortcutkit.security import audit_package


def test_declared_network_example_passes_strict_audit() -> None:
    root = Path(__file__).resolve().parents[3]
    audit = audit_package(root / "shortcuts" / "examples" / "network-note", strict=True)
    assert audit.passed is True
    assert "network" in audit.summary["badges"]
    assert audit.summary["domains"] == ["example.com"]


def test_undeclared_network_fixture_fails_strict_audit() -> None:
    fixture = Path(__file__).parent / "fixtures" / "undeclared-network"
    audit = audit_package(fixture, strict=True)
    assert audit.passed is False
    assert any(finding.id == "mismatch.network.request" for finding in audit.findings)


def test_undeclared_network_domain_fixture_fails_strict_audit() -> None:
    fixture = Path(__file__).parent / "fixtures" / "undeclared-network-domain"
    audit = audit_package(fixture, strict=True)
    assert audit.passed is False
    assert audit.summary["domains"] == ["evil.example"]
    assert any(finding.id == "mismatch.network.domains" for finding in audit.findings)


def test_share_sheet_open_html_permissions_are_detected() -> None:
    root = Path(__file__).resolve().parents[3]
    audit = audit_package(root / "shortcuts" / "open-html-in-safari", strict=True)
    assert audit.passed is True
    assert "files" in audit.summary["badges"]
    assert "url-schemes" in audit.summary["badges"]
    assert any(finding.id == "declared.files.read" for finding in audit.findings)
    assert any(finding.id == "detected.files.read" for finding in audit.findings)
    assert any(finding.id == "declared.url_schemes" for finding in audit.findings)
    assert audit.summary["review_required"] is True


def test_open_html_uses_safari_runtime_with_file_backups() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (
        root / "shortcuts" / "open-html-in-safari" / "src" / "open-html-in-safari.cherri"
    ).read_text(encoding="utf-8")

    assert "getFileDetail(ShortcutInput" in source
    assert "extractArchive(ShortcutInput)" in source
    assert "getFolderContents(ShortcutInput, true)" in source
    assert "Attempting a local bundled render before Safari opens." in source
    assert "Reading single HTML file for Safari render..." in source
    assert "Ready to open in Safari." in source
    assert "getText(@targetFile)" in source
    assert "replaceText(@assetName.text, @assetUrl, @renderHtml, false, false)" in source
    assert "base64Encode(@renderHtml)" in source
    assert "base64Encode(@targetFile)" not in source
    assert 'openURL("data:text/html;base64,{@encodedHtml}")' in source
    assert "waitToReturn()" in source
    assert "uv run shortcutkit html publish path/to/site --provider here-now --run --json" in source
    assert "quicklook(ShortcutInput)" in source
    assert "openFile(ShortcutInput, true)" in source
    assert "Single file resolved to HTML text" in source
    assert "No HTML file found in ZIP." in source
    assert "No HTML file found in folder." in source
    assert source.count('"Open HTML Backup"') == 2
    assert "getFileLink(ShortcutInput)" not in source
    assert "openURL(@fileLink)" not in source
    assert "#define glyph magicWand" in source


def test_html_source_files_are_scanned_for_domains() -> None:
    fixture = Path(__file__).parent / "fixtures" / "html-source-domain"
    audit = audit_package(fixture, strict=True)
    assert audit.passed is False
    assert audit.summary["domains"] == ["evil.example"]
    assert any(finding.id == "mismatch.network.domains" for finding in audit.findings)


def test_open_html_hosted_profile_is_review_metadata_not_runtime_network() -> None:
    root = Path(__file__).resolve().parents[3]
    audit = audit_package(root / "shortcuts" / "open-html-in-safari", strict=True)
    assert audit.passed is True
    assert any(finding.id == "reviewed.html_runtime.hosted" for finding in audit.findings)


def test_native_file_read_fixture_fails_strict_audit() -> None:
    fixture = Path(__file__).parent / "fixtures" / "undeclared-file-read"
    audit = audit_package(fixture, strict=True)
    assert audit.passed is False
    assert "files" in audit.summary["badges"]
    assert any(finding.id == "mismatch.files.read" for finding in audit.findings)


def test_declared_url_scheme_accepts_colon_suffix() -> None:
    fixture = Path(__file__).parent / "fixtures" / "declared-data-url-colon"
    audit = audit_package(fixture, strict=True)
    assert audit.passed is True
    assert any(
        finding.id == "declared.url_schemes" and finding.evidence == ["data"]
        for finding in audit.findings
    )


def test_css_declarations_are_not_detected_as_url_schemes(tmp_path: Path, monkeypatch) -> None:
    package = tmp_path / "shortcut"
    source = package / "src"
    source.mkdir(parents=True)
    (package / "README.md").write_text("# CSS Scheme Fixture\n", encoding="utf-8")
    (source / "style.css").write_text("body{color:red}", encoding="utf-8")
    (package / "shortcut.yml").write_text(
        """
id: com.shortcuts.tests.css-scheme-fixture
name: CSS Scheme Fixture
version: 0.1.0
summary: Fixture for CSS scheme scanning.
category: testing
status: experimental
license: MIT
maintainers:
  - name: test maintainer
source:
  mode: manual
  entrypoint: src/style.css
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
    monkeypatch.setattr(
        "shortcutkit.manifest.find_repo_root",
        lambda _path: Path(__file__).resolve().parents[3],
    )
    monkeypatch.setattr(
        "shortcutkit.security.find_repo_root",
        lambda _path: Path(__file__).resolve().parents[3],
    )

    audit = audit_package(package, strict=True)

    assert audit.passed is True
    assert not any(finding.id == "mismatch.url_schemes" for finding in audit.findings)
