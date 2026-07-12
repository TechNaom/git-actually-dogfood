"""test_core.py -- pytest suite for relnotes.core."""

from datetime import date

import pytest

from relnotes.core import Entry, RelnotesError, add_entry, list_entries, load_entries, save_entries


def test_entry_rejects_unknown_category():
    with pytest.raises(RelnotesError, match="Unknown category"):
        Entry(description="Did a thing", category="nope")


def test_entry_rejects_empty_description():
    with pytest.raises(RelnotesError, match="cannot be empty"):
        Entry(description="   ", category="added")


def test_entry_defaults_to_todays_date():
    entry = Entry(description="Did a thing", category="added")

    assert entry.date == date.today().isoformat()


def test_add_entry_persists_to_store(tmp_path):
    store = tmp_path / "relnotes.json"

    entry = add_entry("Fixed the crash on startup", "fixed", path=store)

    assert store.exists()
    loaded = load_entries(store)
    assert len(loaded) == 1
    assert loaded[0].description == entry.description
    assert loaded[0].category == "fixed"


def test_add_entry_appends_not_overwrites(tmp_path):
    store = tmp_path / "relnotes.json"
    add_entry("First change", "added", path=store)
    add_entry("Second change", "fixed", path=store)

    entries = load_entries(store)

    assert len(entries) == 2


def test_load_entries_missing_file_returns_empty_list(tmp_path):
    store = tmp_path / "does-not-exist.json"

    assert load_entries(store) == []


def test_load_entries_corrupt_json_raises(tmp_path):
    store = tmp_path / "relnotes.json"
    store.write_text("{not valid json")

    with pytest.raises(RelnotesError, match="not valid JSON"):
        load_entries(store)


def test_save_entries_sorts_by_date_then_category(tmp_path):
    store = tmp_path / "relnotes.json"
    entries = [
        Entry(description="Later fix", category="fixed", date="2026-02-01"),
        Entry(description="Earlier add", category="added", date="2026-01-01"),
    ]

    save_entries(entries, store)
    loaded = load_entries(store)

    assert [e.date for e in loaded] == ["2026-01-01", "2026-02-01"]


def test_list_entries_returns_all_in_store(tmp_path):
    store = tmp_path / "relnotes.json"
    add_entry("A", "added", path=store, entry_date="2026-01-01")
    add_entry("B", "removed", path=store, entry_date="2026-01-02")

    entries = list_entries(store)

    assert len(entries) == 2
    assert {e.description for e in entries} == {"A", "B"}


def test_list_entries_can_filter_by_category(tmp_path):
    store = tmp_path / "relnotes.json"
    add_entry("A", "added", path=store, entry_date="2026-01-01")
    add_entry("B", "removed", path=store, entry_date="2026-01-02")

    entries = list_entries(store, category="added")

    assert len(entries) == 1
    assert entries[0].description == "A"
