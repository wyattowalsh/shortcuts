import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Literal, cast
from urllib.parse import urlparse

from shortcutkit.actiondb import action_map, load_actiondb
from shortcutkit.manifest import load_manifest
from shortcutkit.models import ActionEntry, Finding, SecurityAudit
from shortcutkit.paths import find_repo_root, package_root

SEVERITY_BY_RISK = {
    "low": "low",
    "interactive": "medium",
    "sensitive": "medium",
    "high": "high",
    "critical": "critical",
}
Severity = Literal["info", "low", "medium", "high", "critical"]
URL_PATTERN = re.compile(r"https?://[^\s)>'\"]+")
SCHEME_PATTERN = re.compile(r"\b([a-z][a-z0-9+.-]*)://", re.IGNORECASE)


def _permission_enabled(permissions: dict[str, Any], dotted: str) -> bool:
    cursor: Any = permissions
    for part in dotted.split("."):
        if not isinstance(cursor, dict) or part not in cursor:
            return False
        cursor = cursor[part]
    return bool(cursor)


def _declared_schemes(permissions: dict[str, Any]) -> set[str]:
    raw = permissions.get("url_schemes", [])
    if not isinstance(raw, list):
        return set()
    return {str(item).lower().removesuffix("://") for item in raw}


def _normalize_domain(value: str) -> str | None:
    parsed = urlparse(value if "://" in value else f"https://{value}")
    hostname = parsed.hostname
    if hostname is None:
        return None
    return hostname.lower().rstrip(".")


def _declared_domains(permissions: dict[str, Any]) -> set[str]:
    network = permissions.get("network", {})
    if not isinstance(network, dict):
        return set()
    raw = network.get("domains", [])
    if not isinstance(raw, list):
        return set()
    return {domain for item in raw if (domain := _normalize_domain(str(item)))}


def _source_files(root: Path) -> list[Path]:
    source_root = root / "src"
    if not source_root.exists():
        return []
    suffixes = {".md", ".txt", ".json", ".yaml", ".yml", ".shortcutsource", ".cherri", ".jelly"}
    return sorted(
        file_path
        for file_path in source_root.glob("**/*")
        if file_path.is_file() and file_path.suffix.lower() in suffixes
    )


def _evidence_for_action(root: Path, action: ActionEntry) -> list[str]:
    evidence: list[str] = []
    for file_path in _source_files(root):
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        for detector in action.detectors:
            if detector and detector.lower() in text.lower():
                rel = file_path.relative_to(root)
                evidence.append(f"{rel}: {detector}")
    return sorted(set(evidence))


def _domains(root: Path) -> list[str]:
    domains: set[str] = set()
    for file_path in _source_files(root):
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        for match in URL_PATTERN.finditer(text):
            domain = _normalize_domain(match.group(0))
            if domain is not None:
                domains.add(domain)
    return sorted(domains)


def _schemes(root: Path) -> list[str]:
    schemes: set[str] = set()
    for file_path in _source_files(root):
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        schemes.update(match.group(1).lower() for match in SCHEME_PATTERN.finditer(text))
    return sorted(schemes - {"http", "https"})


def _declared_findings(permissions: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    declared = {
        "clipboard.read": "clipboard.read",
        "clipboard.write": "clipboard.write",
        "shell.run": "shell",
        "network.request": "network.allowed",
        "ai.model": "ai.uses_model_action",
    }
    actions = action_map()
    for action_id, permission_path in declared.items():
        if not _permission_enabled(permissions, permission_path):
            continue
        action = actions[action_id]
        findings.append(
            Finding(
                id=f"declared.{action_id}",
                title=f"{action.name} declared",
                severity=cast(Severity, SEVERITY_BY_RISK[action.risk_tier]),
                status="declared",
                detail=action.notes or f"Manifest declares {permission_path}.",
                path="shortcut.yml",
                remediation=action.remediation,
                review_required="two-reviewer"
                if action.risk_tier in {"high", "critical"}
                else "maintainer",
            )
        )
    return findings


def _detected_findings(root: Path, permissions: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    actions = action_map()
    permission_paths = {
        "clipboard.read": "clipboard.read",
        "clipboard.write": "clipboard.write",
        "shell.run": "shell",
        "network.request": "network.allowed",
        "ai.model": "ai.uses_model_action",
        "url-scheme.callback": "url_schemes",
    }
    for action in actions.values():
        evidence = _evidence_for_action(root, action)
        if not evidence:
            continue
        permission_path = permission_paths.get(action.id)
        declared = False
        if permission_path == "url_schemes":
            declared = bool(_declared_schemes(permissions))
        elif permission_path:
            declared = _permission_enabled(permissions, permission_path)
        status = "detected" if declared else "mismatch"
        detail = "Detected source signal matches declared permissions."
        if status == "mismatch":
            detail = f"Detected {action.name} but manifest does not declare {permission_path}."
        findings.append(
            Finding(
                id=f"{status}.{action.id}",
                title=f"Detected {action.name}",
                severity=cast(Severity, SEVERITY_BY_RISK[action.risk_tier]),
                status=status,
                detail=detail,
                path="src",
                remediation=action.remediation,
                review_required="two-reviewer"
                if action.risk_tier in {"high", "critical"}
                else "maintainer",
                evidence=evidence,
            )
        )
    return findings


def _url_scheme_findings(root: Path, permissions: dict[str, Any]) -> list[Finding]:
    declared = _declared_schemes(permissions)
    detected = set(_schemes(root))
    undeclared = sorted(detected - declared)
    if not undeclared:
        return []
    return [
        Finding(
            id="mismatch.url_schemes",
            title="Undeclared URL schemes detected",
            severity="medium",
            status="mismatch",
            detail=f"Source uses undeclared URL schemes: {', '.join(undeclared)}.",
            path="src",
            remediation="Declare every non-HTTP URL scheme in declared_permissions.url_schemes.",
            review_required="maintainer",
            evidence=undeclared,
        )
    ]


def _domain_findings(root: Path, permissions: dict[str, Any]) -> list[Finding]:
    detected = set(_domains(root))
    if not detected:
        return []
    declared = _declared_domains(permissions)
    undeclared = sorted(detected - declared)
    if not undeclared:
        return []
    return [
        Finding(
            id="mismatch.network.domains",
            title="Undeclared network domains detected",
            severity="high",
            status="mismatch",
            detail=f"Source uses undeclared network domains: {', '.join(undeclared)}.",
            path="src",
            remediation="Declare every network domain in declared_permissions.network.domains.",
            review_required="maintainer",
            evidence=undeclared,
        )
    ]


def _artifact_findings(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for artifact in sorted(root.glob("dist/**/*.shortcut")):
        checksum = artifact.with_suffix(artifact.suffix + ".sha256")
        if not checksum.exists():
            findings.append(
                Finding(
                    id="unknown.artifact.checksum",
                    title="Shortcut artifact missing checksum",
                    severity="high",
                    status="unknown",
                    detail=f"{artifact.relative_to(root)} has no .sha256 sidecar.",
                    path=str(artifact.relative_to(root)),
                    remediation=(
                        "Generate release metadata and SHA-256 checksums before distribution."
                    ),
                    review_required="maintainer",
                )
            )
    return findings


def permission_badges(audit: SecurityAudit) -> list[str]:
    badges: set[str] = set()
    for finding in audit.findings:
        if "clipboard" in finding.id:
            badges.add("clipboard")
        if "network" in finding.id:
            badges.add("network")
        if "shell" in finding.id:
            badges.add("shell")
        if "ai.model" in finding.id:
            badges.add("ai")
        if "url" in finding.id:
            badges.add("url-schemes")
    return sorted(badges)


def audit_package(path: Path, *, strict: bool) -> SecurityAudit:
    root = package_root(path)
    manifest = load_manifest(root)
    permissions = manifest.declared_permissions
    actiondb = load_actiondb(str(find_repo_root(root)))
    findings: list[Finding] = []
    findings.extend(_declared_findings(permissions))
    findings.extend(_detected_findings(root, permissions))
    findings.extend(_domain_findings(root, permissions))
    findings.extend(_url_scheme_findings(root, permissions))
    findings.extend(_artifact_findings(root))

    if not (root / "src").exists():
        findings.append(
            Finding(
                id="unknown.source",
                title="Source directory missing",
                severity="high",
                status="unknown",
                detail="Strict mode cannot verify capability signals without source files.",
                path="src",
                remediation="Add source files or mark artifact provenance as reviewed.",
                review_required="maintainer",
            )
        )

    domains = _domains(root)
    severities = Counter(finding.severity for finding in findings)
    blocking = [
        finding
        for finding in findings
        if finding.status in {"unknown", "mismatch"}
        or finding.severity in {"high", "critical"}
        and finding.status == "detected"
    ]
    return SecurityAudit(
        package_id=manifest.id,
        actiondb_version=actiondb.version,
        strict=strict,
        passed=not (strict and blocking),
        summary={
            "badges": permission_badges(
                SecurityAudit(
                    package_id=manifest.id,
                    actiondb_version=actiondb.version,
                    strict=strict,
                    passed=True,
                    findings=findings,
                )
            ),
            "domains": domains,
            "finding_counts": dict(sorted(severities.items())),
            "review_required": any(f.review_required == "two-reviewer" for f in findings),
        },
        findings=findings,
    )


def audit_json(audit: SecurityAudit) -> str:
    return json.dumps(audit.model_dump(), indent=2, sort_keys=True) + "\n"
