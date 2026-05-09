from pathlib import Path

from shortcutkit.catalog import catalog_payload
from shortcutkit.paths import find_repo_root


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
        lines.extend(
            [
                f"## {item['name']}",
                "",
                f"- ID: `{item['id']}`",
                f"- Version: `{item['version']}`",
                f"- Status: `{item['status']}`",
                f"- Path: `{item['path']}`",
                f"- Security tier: `{item['security_tier']}`",
                f"- Permission badges: `{', '.join(item['permission_badges']) or 'none'}`",
                f"- Review required: `{review_required}`",
                "",
                str(item["summary"]),
                "",
            ]
        )
    return "\n".join(lines)
