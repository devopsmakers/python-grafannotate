import pytest
from click.testing import CliRunner
from grafannotate import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner, caplog):
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'NewConnectionError' in caplog.text
