from __future__ import annotations

from pathlib import Path

BLOCKED_TERMS = {
    "GPL-2.0",
    "GPL-3.0",
    "AGPL",
    "non-commercial",
    "noncommercial",
}
SCAN_ROOTS = [Path("packages"), Path("app-intents"), Path("shortcuts/examples")]


def main() -> int:
    violations: list[str] = []
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {
                ".py",
                ".json",
                ".md",
                ".yml",
                ".yaml",
                ".swift",
            }:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for term in BLOCKED_TERMS:
                if term.lower() in text.lower():
                    violations.append(f"{path}: blocked license term {term}")
    if violations:
        print("license policy failed")
        for violation in violations:
            print(f"- {violation}")
        return 1
    print("license policy passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
