from pathlib import Path


def test_workspace_has_required_roots() -> None:
    root = Path(__file__).resolve().parents[1]
    for relative in ["packages/shortcutkit", "packages/schemas", "shortcuts/examples", "apps/docs"]:
        assert (root / relative).exists(), relative
