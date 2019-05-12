import pytest
import sys
from click.testing import CliRunner
from grafannotate import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner, caplog):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Events must have at least one tag' in caplog.text


def test_cli_with_tag(runner, caplog, monkeypatch):
    monkeypatch.setattr(sys.stdin, 'isatty', True)
    result = runner.invoke(cli.main, ['--tag', 'event'])
    assert result.exit_code == 0
    assert 'NewConnectionError' in caplog.text


def test_cli_with_bad_end_time(runner, caplog):
    result = runner.invoke(cli.main, ['--tag', 'event', '--end', 0])
    assert result.exit_code == 0
    assert 'end time cannot be before start time' in caplog.text


def test_cli_with_bad_uri(runner, caplog):
    result = runner.invoke(cli.main, ['--tag', 'event', '--uri', 'blob://localhost'])
    assert result.exit_code == 0
    assert 'Scheme blob not recognised' in caplog.text
