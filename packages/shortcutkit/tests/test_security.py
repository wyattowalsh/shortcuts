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
