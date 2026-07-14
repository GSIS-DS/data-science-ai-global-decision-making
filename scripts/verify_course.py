"""Run lightweight structural checks for the public course repository."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_COLUMNS = {
    "country", "iso3", "year", "gdp_growth", "inflation", "exports_usd_bn",
    "imports_usd_bn", "trade_openess_percent", "unemployment_percent",
    "exchange_rate_change_percent", "internet_users_percent", "co2_per_capita", "region",
}
REQUIRED_NOTEBOOKS = [
    ROOT / "notebooks/week-01/01_data_ai_evidence_global_decision_making.ipynb",
    ROOT / "notebooks/week-02/02_working_with_data_in_python.ipynb",
    ROOT / "notebooks/week-03/03_cleaning_transforming_data.ipynb",
    ROOT / "notebooks/week-04/04_combining_reshaping_global_data.ipynb",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_data() -> None:
    path = ROOT / "data/sample/global_indicators_sample.csv"
    if not path.exists():
        fail(f"Missing sample dataset: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    missing = REQUIRED_COLUMNS - set(rows[0] if rows else {})
    if missing:
        fail(f"Sample CSV missing columns: {sorted(missing)}")
    if not 30 <= len(rows) <= 40:
        fail(f"Expected 30-40 sample rows, found {len(rows)}")
    print(f"OK: sample CSV has {len(rows)} rows and all required columns")


def validate_notebooks() -> None:
    for path in REQUIRED_NOTEBOOKS:
        if not path.exists():
            fail(f"Missing required notebook: {path.relative_to(ROOT)}")
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"Invalid notebook JSON in {path.relative_to(ROOT)}: {exc}")
        if notebook.get("nbformat") != 4 or not isinstance(notebook.get("cells"), list):
            fail(f"Invalid notebook structure: {path.relative_to(ROOT)}")
        source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
        if "raw.githubusercontent.com/GSIS-DS/" not in source:
            fail(f"Notebook lacks Colab-safe public data fallback: {path.relative_to(ROOT)}")
        print(f"OK: valid Colab-aware notebook {path.relative_to(ROOT)}")


def validate_local_markdown_links() -> None:
    link_pattern = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
    broken: list[str] = []
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", ".venv"} for part in path.parts):
            continue
        for target in link_pattern.findall(path.read_text(encoding="utf-8")):
            target = unquote(target.strip().strip("<>").split("#", 1)[0])
            if not target or re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
                continue
            if not (path.parent / target).resolve().exists():
                broken.append(f"{path.relative_to(ROOT)} -> {target}")
    if broken:
        fail("Broken local Markdown links:\n" + "\n".join(broken))
    print("OK: local Markdown links resolve")


def validate_outdated_terms() -> None:
    forbidden = ["GSIS-DS-Fall-2026", "ungraded diagnostic", "diagnostic only"]
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".git", ".venv"} for part in path.parts):
            continue
        if path.name in {"agent-instructions", "agent-instructions-2", "verify_course.py"} or path.suffix == ".ipynb":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for term in forbidden:
            if term.lower() in text.lower():
                hits.append(f"{path.relative_to(ROOT)} contains {term!r}")
    if hits:
        fail("Outdated terminology found:\n" + "\n".join(hits))
    print("OK: no outdated course terminology")


if __name__ == "__main__":
    validate_data()
    validate_notebooks()
    validate_local_markdown_links()
    validate_outdated_terms()
    print("All course repository checks passed.")
