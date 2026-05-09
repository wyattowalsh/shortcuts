import json
from pathlib import Path

from shortcutkit.cli import app
from typer.testing import CliRunner


def test_test_command_runs_lint_before_runtime() -> None:
    root = Path(__file__).resolve().parents[3]
    result = CliRunner().invoke(
        app,
        ["test", str(root / "packages" / "shortcutkit" / "tests" / "fixtures" / "no-readme")],
    )
    assert result.exit_code == 1
    assert "lint failed" not in result.output
    assert "missing README.md" in result.output


def test_security_audit_accepts_optional_package_path() -> None:
    root = Path(__file__).resolve().parents[3]
    result = CliRunner().invoke(
        app,
        ["security", "audit", str(root / "shortcuts" / "open-html-in-safari"), "--strict"],
    )
    assert result.exit_code == 0
    assert "security audit passed: com.shortcuts.open-html-in-safari" in result.output


def test_test_command_json_outputs_parseable_json() -> None:
    root = Path(__file__).resolve().parents[3]
    result = CliRunner().invoke(
        app,
        ["test", str(root / "shortcuts" / "open-html-in-safari"), "--json"],
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["package_id"] == "com.shortcuts.open-html-in-safari"
    assert payload["status"] == "disabled"


def test_build_command_json_outputs_parseable_json() -> None:
    root = Path(__file__).resolve().parents[3]
    result = CliRunner().invoke(
        app,
        ["build", str(root / "shortcuts" / "open-html-in-safari"), "--json"],
    )
    assert result.exit_code in {0, 1}
    payload = json.loads(result.output)
    assert payload["package_id"] == "com.shortcuts.open-html-in-safari"
    assert payload["status"] in {"skipped", "unavailable"}


def test_html_analyze_json_reports_supported_local_bundle() -> None:
    fixture = Path(__file__).parent / "fixtures" / "html-supported" / "index.html"
    result = CliRunner().invoke(app, ["html", "analyze", str(fixture), "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["profile"] == "local-bundled"
    assert payload["status"] == "supported"
    assert payload["size_gate"] == "green"
    assert {asset["source"] for asset in payload["assets"]} == {"styles.css", "app.js"}


def test_html_analyze_rejects_external_runtime_assets() -> None:
    fixture = Path(__file__).parent / "fixtures" / "html-external" / "index.html"
    result = CliRunner().invoke(app, ["html", "analyze", str(fixture), "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["status"] == "unsupported"
    assert payload["diagnostics"][0]["id"] == "unsupported.external-reference"


def test_html_bundle_writes_single_file_output(tmp_path: Path) -> None:
    fixture = Path(__file__).parent / "fixtures" / "html-supported" / "index.html"
    output = tmp_path / "index.bundled.html"
    result = CliRunner().invoke(
        app,
        ["html", "bundle", str(fixture), "--output", str(output), "--json"],
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    bundled = output.read_text(encoding="utf-8")
    assert payload["status"] == "bundled"
    assert payload["sha256"]
    assert "<style>" in bundled
    assert "<script>" in bundled
    assert "styles.css" not in bundled
    assert "app.js" not in bundled


def test_html_publish_dry_run_does_not_publish() -> None:
    fixture = Path(__file__).parent / "fixtures" / "html-supported"
    result = CliRunner().invoke(
        app,
        ["html", "publish", str(fixture), "--provider", "here-now", "--dry-run", "--json"],
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["status"] == "dry-run"
    assert payload["dry_run"] is True
    assert {file["path"] for file in payload["files"]} == {"app.js", "index.html", "styles.css"}
