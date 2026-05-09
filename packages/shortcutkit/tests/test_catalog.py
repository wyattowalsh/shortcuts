from pathlib import Path

from shortcutkit.catalog import render_catalog


def test_catalog_contains_clean_clipboard() -> None:
    root = Path(__file__).resolve().parents[3]
    output = render_catalog(root)
    assert "com.shortcuts.examples.clean-clipboard" in output
    assert "shortcuts/examples/clean-clipboard" in output
