import shutil
from pathlib import Path

from shortcutkit.catalog import catalog_payload
from shortcutkit.paths import find_repo_root


def sync_catalog_icon_assets(
    docs_root: Path,
    root: Path | None = None,
    *,
    check: bool = False,
) -> list[Path]:
    repo = root or find_repo_root()
    stale: list[Path] = []
    payload = catalog_payload(repo)
    for item in payload["shortcuts"]:
        icon = item.get("icon")
        if not icon:
            continue
        source = repo / item["path"] / icon["path"]
        target = docs_root / "public" / icon["docs_path"].lstrip("/")
        if check:
            if not target.exists() or target.read_bytes() != source.read_bytes():
                stale.append(target)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    return stale


def generated_reference(root: Path | None = None) -> str:
    repo = root or find_repo_root()
    payload = catalog_payload(repo)
    lines = [
        "---",
        "title: Catalog Reference",
        "description: Generated shortcut catalog reference.",
        "generated: true",
        "---",
        "",
        "# Catalog Reference",
        "",
    ]
    for item in payload["shortcuts"]:
        review_required = "true" if item["review_required"] else "false"
        icon = item.get("icon")
        if icon:
            lines.extend(
                [
                    f"## {item['name']}",
                    "",
                    f"![{icon['alt']}]({icon['docs_path']})",
                    "",
                ]
            )
        else:
            lines.extend([f"## {item['name']}", ""])
        lines.extend(
            [
                f"- ID: `{item['id']}`",
                f"- Version: `{item['version']}`",
                f"- Status: `{item['status']}`",
                f"- Path: `{item['path']}`",
                f"- Security tier: `{item['security_tier']}`",
                f"- Permission badges: `{', '.join(item['permission_badges']) or 'none'}`",
                f"- Review required: `{review_required}`",
                *(
                    [
                        f"- Icon: `{icon['path']}`",
                        f"- Icon SHA-256: `{icon['sha256']}`",
                    ]
                    if icon
                    else []
                ),
                "",
                str(item["summary"]),
                "",
            ]
        )
        html_runtime = item.get("html_runtime")
        if isinstance(html_runtime, dict) and html_runtime.get("profiles"):
            lines.extend(["### HTML Runtime", ""])
            for profile in html_runtime["profiles"]:
                provider = f" via `{profile['provider']}`" if profile.get("provider") else ""
                notes = f" {profile['notes']}" if profile.get("notes") else ""
                lines.append(
                    f"- `{profile['id']}`: `{profile['support']}`{provider}.{notes}".rstrip()
                )
            lines.append("")
    return "\n".join(lines)
