import tempfile

from click.testing import CliRunner

from newshomepages import shoot

TEMP_DIR = tempfile.gettempdir()


def test_single():
    """Test a single screenshot."""
    runner = CliRunner()
    result = runner.invoke(shoot.cli, ["single", "latimes", "-o", TEMP_DIR])
    assert result.exit_code == 0
