import pytest
import time

from click.testing import CliRunner
from grafannotate import cli

CURRENT_TIMESTAMP = int(time.time())


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner, caplog):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'must have at least one tag' in caplog.text


def test_cli_with_tag(runner, caplog):
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


def test_cli_with_user_pass(runner, caplog):
    result = runner.invoke(cli.main, ['--tag', 'event', '--uri', 'http://user:pass@localhost'])
    assert result.exit_code == 0
    assert 'NewConnectionError' in caplog.text


def test_cli_with_api_key(runner, caplog):
    result = runner.invoke(cli.main, ['--tag', 'event', '--uri', 'http://localhost', '--api-key', 'aTestKey'])
    assert result.exit_code == 0
    assert 'NewConnectionError' in caplog.text


def test_cli_with_end_time(runner, caplog):
    result = runner.invoke(cli.main, ['--tag', 'event', '--end', CURRENT_TIMESTAMP + 600])
    assert result.exit_code == 0
    assert 'NewConnectionError' in caplog.text


def test_cli_with_influx(runner, caplog):
    result = runner.invoke(cli.main, ['--tag', 'event', '--uri', 'influx://localhost:8086'])
    assert result.exit_code == 0
    assert 'NewConnectionError' in caplog.text
