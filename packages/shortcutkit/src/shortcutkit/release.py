import hashlib
import json
import subprocess
from pathlib import Path

from shortcutkit.adapters import build_package
from shortcutkit.manifest import load_manifest, load_manifest_data
from shortcutkit.models import ReleaseMetadata
from shortcutkit.paths import package_root
from shortcutkit.security import audit_package, permission_badges


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def current_commit(root: Path) -> str | None:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return completed.stdout.strip()


def release_metadata(path: Path) -> ReleaseMetadata:
    root = package_root(path)
    manifest = load_manifest(root)
    artifacts = []
    for artifact in sorted((root / "dist").glob("*.shortcut")) if (root / "dist").exists() else []:
        artifacts.append(
            {
                "path": str(artifact.relative_to(root)),
                "sha256": sha256_file(artifact),
                "bytes": artifact.stat().st_size,
            }
        )
    return ReleaseMetadata(
        package_id=manifest.id,
        version=manifest.version,
        source_commit=current_commit(root),
        manifest=load_manifest_data(root),
        audit=audit_package(root, strict=False),
        artifacts=artifacts,
        build=build_package(root),
    )


def release_metadata_json(metadata: ReleaseMetadata) -> str:
    return json.dumps(metadata.model_dump(), indent=2, sort_keys=True) + "\n"


def release_notes(path: Path) -> str:
    metadata = release_metadata(path)
    badges = ", ".join(permission_badges(metadata.audit)) or "none"
    review_required = "true" if metadata.audit.summary.get("review_required", False) else "false"
    artifact_lines = ["- No `.shortcut` artifacts are packaged yet."]
    if metadata.artifacts:
        artifact_lines = [
            f"- `{artifact['path']}` SHA-256 `{artifact['sha256']}`"
            for artifact in metadata.artifacts
        ]
    lines = [
        f"# {metadata.manifest['name']} {metadata.version}",
        "",
        f"Package ID: `{metadata.package_id}`",
        f"Source commit: `{metadata.source_commit or 'unknown'}`",
        f"Permission badges: {badges}",
        f"Security audit: {'passed' if metadata.audit.passed else 'review required'}",
        "",
        "## Install",
        "",
        (
            "Import the reviewed `.shortcut` artifact from this release only after verifying "
            "the checksum below. The repository manifest and source remain the source of truth."
        ),
        "",
        "## Artifacts",
        "",
        *artifact_lines,
        "",
        "## Risk Summary",
        "",
        f"- ActionDB version: `{metadata.audit.actiondb_version}`",
        f"- Review required: `{review_required}`",
        f"- Network domains: `{', '.join(metadata.audit.summary.get('domains', [])) or 'none'}`",
        "",
    ]
    return "\n".join(lines)
