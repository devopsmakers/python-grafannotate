import pytest
from click.testing import CliRunner
from grafannotate import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner, caplog):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Events must have at least one tag' in caplog.text


def test_cli_with_tag(runner, caplog):
    result = runner.invoke(cli.main, ['--tag', 'event'])
    assert result.exit_code == 0
    assert 'NewConnectionError' in caplog.text
