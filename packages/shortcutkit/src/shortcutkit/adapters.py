import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from shortcutkit.manifest import load_manifest
from shortcutkit.models import AdapterCapabilities, AdapterInfo, BuildMetadata
from shortcutkit.paths import package_root


def source_hash(root: Path) -> str:
    digest = hashlib.sha256()
    source = root / "src"
    if not source.exists():
        return hashlib.sha256(b"").hexdigest()
    for file_path in sorted(path for path in source.glob("**/*") if path.is_file()):
        digest.update(str(file_path.relative_to(root)).encode())
        digest.update(b"\0")
        digest.update(file_path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def adapter_infos() -> list[AdapterInfo]:
    return [
        AdapterInfo(
            id="manual",
            name="Manual Shortcut Builder",
            available=True,
            capabilities=AdapterCapabilities(
                build=True, export=False, inspect=True, test=False, license="MIT"
            ),
            notes="Documents manual build steps without compiling artifacts.",
        ),
        AdapterInfo(
            id="artifact",
            name="Prebuilt Artifact Adapter",
            available=True,
            capabilities=AdapterCapabilities(
                build=False, export=True, inspect=True, test=True, license="MIT"
            ),
            notes="Uses checked release artifacts and provenance metadata.",
        ),
        AdapterInfo(
            id="cherri",
            name="Cherri External Adapter",
            binary="cherri",
            available=shutil.which("cherri") is not None,
            capabilities=AdapterCapabilities(
                build=True, export=True, inspect=False, test=False, license="external"
            ),
            install="Install Cherri separately and ensure `cherri` is on PATH.",
            notes="Runs an external Cherri binary; compiler code is not vendored.",
        ),
        AdapterInfo(
            id="jelly",
            name="Jellycuts External Adapter",
            binary="jelly",
            available=shutil.which("jelly") is not None,
            capabilities=AdapterCapabilities(
                build=True, export=True, inspect=False, test=False, license="external"
            ),
            install="Install Jellycuts separately and ensure `jelly` is on PATH.",
            notes="Runs an external Jellycuts binary; compiler code is not vendored.",
        ),
    ]


def adapter_map() -> dict[str, AdapterInfo]:
    return {adapter.id: adapter for adapter in adapter_infos()}


def adapters_json() -> str:
    return (
        json.dumps([adapter.model_dump() for adapter in adapter_infos()], indent=2, sort_keys=True)
        + "\n"
    )


def _artifact_stem(name: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9 ._-]+", " ", name).strip(" ._-")
    stem = re.sub(r"\s+", " ", stem)
    return stem or "Shortcut"


def _entrypoint_under_root(root: Path, entrypoint: str | None) -> Path | None:
    if not entrypoint:
        return None
    candidate = Path(entrypoint)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    resolved_root = root.resolve()
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError:
        return None
    return resolved


def build_package(path: Path, *, run_external: bool = False) -> BuildMetadata:
    root = package_root(path)
    manifest = load_manifest(root)
    adapter = adapter_map().get(manifest.source.mode)
    if adapter is None:
        return BuildMetadata(
            package_id=manifest.id,
            adapter_id=manifest.source.mode,
            source_hash=source_hash(root),
            status="unavailable",
            message=f"No adapter registered for source mode {manifest.source.mode}.",
        )

    if manifest.source.mode == "manual":
        return BuildMetadata(
            package_id=manifest.id,
            adapter_id=adapter.id,
            source_hash=source_hash(root),
            status="manual",
            message="Manual source mode is valid; build by following src/shortcut.md instructions.",
        )

    if manifest.source.mode == "artifact":
        artifact = _entrypoint_under_root(root, manifest.source.entrypoint)
        if artifact is None:
            return BuildMetadata(
                package_id=manifest.id,
                adapter_id=adapter.id,
                source_hash=source_hash(root),
                status="unavailable",
                message="Artifact entrypoint must be a relative path inside the package.",
            )
        if not artifact.exists():
            return BuildMetadata(
                package_id=manifest.id,
                adapter_id=adapter.id,
                source_hash=source_hash(root),
                status="unavailable",
                message=f"Artifact entrypoint is missing: {artifact.relative_to(root)}.",
            )
        return BuildMetadata(
            package_id=manifest.id,
            adapter_id=adapter.id,
            source_hash=source_hash(root),
            artifact_path=str(artifact.relative_to(root)),
            status="skipped",
            message="Artifact mode uses existing artifact; no compilation was run.",
        )

    entrypoint = _entrypoint_under_root(root, manifest.source.entrypoint)
    if entrypoint is None:
        return BuildMetadata(
            package_id=manifest.id,
            adapter_id=adapter.id,
            source_hash=source_hash(root),
            status="unavailable",
            message="External adapter entrypoint must be a relative path inside the package.",
        )

    if not adapter.available or adapter.binary is None:
        return BuildMetadata(
            package_id=manifest.id,
            adapter_id=adapter.id,
            source_hash=source_hash(root),
            status="unavailable",
            message=adapter.install or f"Install {adapter.id} and retry.",
        )
    artifact_path: Path | None = None
    command = [adapter.binary, str(entrypoint)]
    if adapter.id == "cherri":
        artifact_path = root / "dist" / f"{_artifact_stem(manifest.name)}.shortcut"
        command.append("--derive-uuids")
        command.append(f"--output={artifact_path}")
    if not run_external:
        return BuildMetadata(
            package_id=manifest.id,
            adapter_id=adapter.id,
            command=command,
            environment={"PATH": os.environ.get("PATH", "")},
            source_hash=source_hash(root),
            status="skipped",
            message="External adapter command resolved; pass --run-external to execute it.",
        )
    if adapter.id == "cherri" and artifact_path is not None:
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(command, cwd=root, check=True)
    if adapter.id == "cherri":
        unsigned_sidecar = entrypoint.parent / f"{_artifact_stem(manifest.name)}_unsigned.shortcut"
        source_dir = entrypoint.parent.resolve()
        unsigned_sidecar = unsigned_sidecar.resolve()
        if (
            unsigned_sidecar.exists()
            and unsigned_sidecar != artifact_path
            and unsigned_sidecar.parent == source_dir
        ):
            unsigned_sidecar.unlink()
    return BuildMetadata(
        package_id=manifest.id,
        adapter_id=adapter.id,
        command=command,
        environment={"PATH": os.environ.get("PATH", "")},
        source_hash=source_hash(root),
        artifact_path=str(artifact_path.relative_to(root)) if artifact_path else None,
        status="built",
        message="External adapter completed successfully.",
    )
