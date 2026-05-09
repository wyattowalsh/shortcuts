import json
from pathlib import Path

from shortcutkit.catalog import render_catalog
from shortcutkit.docs import sync_catalog_icon_assets


def test_catalog_contains_clean_clipboard() -> None:
    root = Path(__file__).resolve().parents[3]
    output = render_catalog(root)
    assert "com.shortcuts.examples.clean-clipboard" in output
    assert "shortcuts/examples/clean-clipboard" in output


def test_catalog_contains_real_shortcuts_outside_examples() -> None:
    root = Path(__file__).resolve().parents[3]
    output = render_catalog(root)
    assert "com.shortcuts.open-html-in-safari" in output
    assert "shortcuts/open-html-in-safari" in output


def test_catalog_includes_declared_icon_metadata() -> None:
    root = Path(__file__).resolve().parents[3]
    payload = json.loads(render_catalog(root))
    shortcut = next(
        item for item in payload["shortcuts"] if item["id"] == "com.shortcuts.open-html-in-safari"
    )

    assert shortcut["icon"]["path"] == "icon.png"
    assert (
        shortcut["icon"]["sha256"]
        == "4413115dfe470147c8240fa8e0231469032adb24f579db2e708e218b65fdd702"
    )
    assert shortcut["icon"]["docs_path"] == "/catalog-icons/com.shortcuts.open-html-in-safari.png"


def test_docs_icon_sync_copies_declared_icon(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[3]
    stale = sync_catalog_icon_assets(tmp_path, root, check=True)
    assert stale == [
        tmp_path / "public" / "catalog-icons" / "com.shortcuts.open-html-in-safari.png"
    ]

    sync_catalog_icon_assets(tmp_path, root)

    target = tmp_path / "public" / "catalog-icons" / "com.shortcuts.open-html-in-safari.png"
    assert (
        target.read_bytes()
        == (root / "shortcuts" / "open-html-in-safari" / "icon.png").read_bytes()
    )
    assert sync_catalog_icon_assets(tmp_path, root, check=True) == []


def test_catalog_includes_html_runtime_metadata() -> None:
    root = Path(__file__).resolve().parents[3]
    payload = json.loads(render_catalog(root))
    shortcut = next(
        item for item in payload["shortcuts"] if item["id"] == "com.shortcuts.open-html-in-safari"
    )
    profiles = {profile["id"]: profile for profile in shortcut["html_runtime"]["profiles"]}
    assert profiles["local-bundled"]["support"] == "constrained"
    assert profiles["hosted"]["provider"] == "here-now"
