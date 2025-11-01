import json
import re
from pathlib import Path

import yaml
from typer.testing import CliRunner

from fastapi_openapi_cli.cli import app

runner = CliRunner()


def strip_ansi_codes(text: str) -> str:
    """
    Remove ANSI escape sequences from text.

    This is necessary because Typer uses Rich for formatting, and Rich doesn't
    respect Click's CliRunner color parameter. This is a known issue:
    https://github.com/ewels/rich-click/issues/232

    Uses the standard regex pattern for ANSI escape sequences.
    """
    ansi_escape_pattern = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape_pattern.sub("", text)


def test_export_to_stdout():
    result = runner.invoke(app, ["--app", "tests.fixtures.sample_app:app"])

    assert result.exit_code == 0
    spec = json.loads(result.stdout)
    assert spec["info"]["title"] == "Sample API"


def test_export_to_json_file(tmp_path: Path):
    output_file = tmp_path / "spec.json"
    result = runner.invoke(app, ["--app", "tests.fixtures.sample_app:app", "-o", str(output_file)])

    assert result.exit_code == 0
    assert output_file.exists()

    with output_file.open() as f:
        spec = json.load(f)

    assert spec["info"]["title"] == "Sample API"


def test_export_to_yaml_file(tmp_path: Path):
    output_file = tmp_path / "spec.yaml"
    result = runner.invoke(app, ["--app", "tests.fixtures.sample_app:app", "-o", str(output_file)])

    assert result.exit_code == 0
    assert output_file.exists()

    with output_file.open() as f:
        spec = yaml.safe_load(f)

    assert spec["info"]["title"] == "Sample API"


def test_export_with_invalid_app_path():
    result = runner.invoke(app, ["--app", "nonexistent.module:app"])

    assert result.exit_code != 0
    assert "Could not import module" in result.output


def test_export_help():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    # Strip ANSI codes since Rich doesn't respect CliRunner's color parameter
    clean_output = strip_ansi_codes(result.stdout)
    assert "export" in clean_output.lower()
    assert "--app" in clean_output
