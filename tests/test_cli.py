"""test_cli.py -- pytest suite for relnotes.cli, the argparse entry point."""

import pytest

from relnotes.cli import main


def _add(store, description, category, entry_date):
    return main(
        ["--file", str(store), "add", description, "--category", category, "--date", entry_date]
    )


def test_add_then_list(tmp_path, capsys):
    store = tmp_path / "relnotes.json"

    exit_code = _add(store, "Fixed the login bug", "fixed", "2026-01-05")
    assert exit_code == 0

    exit_code = main(["--file", str(store), "list"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "fixed: Fixed the login bug" in out


def test_list_empty_store_prints_hint(tmp_path, capsys):
    store = tmp_path / "relnotes.json"

    exit_code = main(["--file", str(store), "list"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "No entries yet" in out


def test_add_invalid_category_rejected_by_argparse(tmp_path):
    store = tmp_path / "relnotes.json"

    with pytest.raises(SystemExit):
        main(["--file", str(store), "add", "Something", "--category", "nonsense"])


def test_list_filters_by_category(tmp_path, capsys):
    store = tmp_path / "relnotes.json"
    _add(store, "Fixed the login bug", "fixed", "2026-01-05")
    _add(store, "Added dark mode", "added", "2026-01-06")
    capsys.readouterr()  # drain the "Added [...]" output from the two adds above

    exit_code = main(["--file", str(store), "list", "--category", "fixed"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "Fixed the login bug" in out
    assert "Added dark mode" not in out


def test_list_category_with_no_matches_prints_hint(tmp_path, capsys):
    store = tmp_path / "relnotes.json"
    _add(store, "Added dark mode", "added", "2026-01-06")
    capsys.readouterr()  # drain the "Added [...]" output from the add above

    exit_code = main(["--file", str(store), "list", "--category", "security"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "No entries in category 'security'" in out


def test_list_invalid_category_rejected_by_argparse(tmp_path):
    store = tmp_path / "relnotes.json"

    with pytest.raises(SystemExit):
        main(["--file", str(store), "list", "--category", "nonsense"])


def test_render_markdown_default(tmp_path, capsys):
    store = tmp_path / "relnotes.json"
    _add(store, "Added dark mode", "added", "2026-01-05")

    exit_code = main(["--file", str(store), "render"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "# Changelog" in out
    assert "## Added" in out


def test_render_plain_format(tmp_path, capsys):
    store = tmp_path / "relnotes.json"
    _add(store, "Added dark mode", "added", "2026-01-05")

    exit_code = main(["--file", str(store), "render", "--format", "plain"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "[2026-01-05] added: Added dark mode" in out


def test_render_html_not_yet_supported(tmp_path):
    store = tmp_path / "relnotes.json"

    with pytest.raises(SystemExit):
        main(["--file", str(store), "render", "--format", "html"])
