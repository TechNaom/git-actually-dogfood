"""
relnotes.core -- entry storage and validation.

Deliberately kept separate from cli.py: this module knows nothing about
argparse, sys.argv, or printing to a terminal. It's a plain JSON-backed
store of changelog entries, testable without a terminal attached.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

VALID_CATEGORIES = ("added", "changed", "fixed", "removed", "security")

DEFAULT_STORE_PATH = Path("relnotes.json")


class RelnotesError(Exception):
    """Raised for any user-facing error (bad category, missing store, corrupt file)."""


@dataclass
class Entry:
    description: str
    category: str
    date: str = field(default_factory=lambda: date.today().isoformat())

    def __post_init__(self) -> None:
        self.category = self.category.lower()
        if self.category not in VALID_CATEGORIES:
            raise RelnotesError(
                f"Unknown category {self.category!r}. "
                f"Valid categories are: {', '.join(VALID_CATEGORIES)}."
            )
        if not self.description.strip():
            raise RelnotesError("Entry description cannot be empty.")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Entry":
        return cls(description=data["description"], category=data["category"], date=data["date"])


def load_entries(path: Path = DEFAULT_STORE_PATH) -> list[Entry]:
    """Load entries from a JSON store. Returns an empty list if the file doesn't exist yet."""
    path = Path(path)
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RelnotesError(f"{path} is not valid JSON: {exc}") from exc
    return [Entry.from_dict(item) for item in raw]


def save_entries(entries: list[Entry], path: Path = DEFAULT_STORE_PATH) -> None:
    """Write entries back to the JSON store, sorted by date then category."""
    path = Path(path)
    ordered = sorted(entries, key=lambda e: (e.date, e.category))
    path.write_text(
        json.dumps([e.to_dict() for e in ordered], indent=2) + "\n",
        encoding="utf-8",
    )


def add_entry(
    description: str,
    category: str,
    path: Path = DEFAULT_STORE_PATH,
    entry_date: str | None = None,
) -> Entry:
    """Create a new entry, append it to the store, and return it."""
    kwargs = {"description": description, "category": category}
    if entry_date is not None:
        kwargs["date"] = entry_date
    entry = Entry(**kwargs)
    entries = load_entries(path)
    entries.append(entry)
    save_entries(entries, path)
    return entry


def list_entries(path: Path = DEFAULT_STORE_PATH, category: str | None = None) -> list[Entry]:
    """
    Return entries, sorted by date then category.

    If `category` is given, only entries in that category are returned.
    """
    entries = load_entries(path)
    if category is not None:
        entries = [e for e in entries if e.category == category]
    return entries
