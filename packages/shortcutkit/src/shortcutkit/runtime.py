import json
import platform
import shutil
import subprocess
from pathlib import Path

from shortcutkit.manifest import load_manifest
from shortcutkit.models import RuntimeTestResult
from shortcutkit.paths import package_root


def runtime_test_package(path: Path, *, run: bool = False) -> RuntimeTestResult:
    root = package_root(path)
    manifest = load_manifest(root)
    runtime = (manifest.tests or {}).get("runtime", {})
    if not runtime.get("enabled", False):
        return RuntimeTestResult(
            package_id=manifest.id,
            status="disabled",
            requires_macos=True,
            message="Runtime tests are disabled in shortcut.yml.",
        )
    if platform.system() != "Darwin":
        return RuntimeTestResult(
            package_id=manifest.id,
            status="skipped",
            requires_macos=True,
            message="Runtime tests require macOS and are skipped on this platform.",
        )
    shortcuts_bin = shutil.which("shortcuts")
    if shortcuts_bin is None:
        return RuntimeTestResult(
            package_id=manifest.id,
            status="skipped",
            requires_macos=True,
            message="Apple `shortcuts` CLI is not available on PATH.",
        )
    shortcut_name = str(runtime.get("shortcut_name", manifest.name))
    command = [shortcuts_bin, "run", shortcut_name]
    if not run:
        return RuntimeTestResult(
            package_id=manifest.id,
            status="skipped",
            requires_macos=True,
            command=command,
            message="Runtime command resolved; pass --run to execute it.",
        )
    completed = subprocess.run(command, cwd=root, check=False, capture_output=True, text=True)
    return RuntimeTestResult(
        package_id=manifest.id,
        status="passed" if completed.returncode == 0 else "failed",
        requires_macos=True,
        command=command,
        stdout=completed.stdout,
        stderr=completed.stderr,
        exit_code=completed.returncode,
        message="Runtime command completed.",
    )


def runtime_result_json(result: RuntimeTestResult) -> str:
    return json.dumps(result.model_dump(), indent=2, sort_keys=True) + "\n"
