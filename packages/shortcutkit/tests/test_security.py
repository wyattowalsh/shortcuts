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


def test_open_html_uses_safari_runtime_without_picker_handoff() -> None:
    root = Path(__file__).resolve().parents[3]
    source = (
        root / "shortcuts" / "open-html-in-safari" / "src" / "open-html-in-safari.cherri"
    ).read_text(encoding="utf-8")

    assert "getText(ShortcutInput)" in source
    assert "base64Encode(@htmlText)" in source
    assert 'openURL("data:text/html;base64,{@encodedHtml}")' in source
    assert source.count("showNotification(") == 1
    assert "getFileLink(ShortcutInput)" not in source
    assert "openURL(@fileLink)" not in source
    assert "quicklook(" not in source
    assert "openFile(" not in source
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
