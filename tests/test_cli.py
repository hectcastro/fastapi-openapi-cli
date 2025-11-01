import json
from pathlib import Path

import yaml
from typer.testing import CliRunner

from fastapi_openapi_cli.cli import app

runner = CliRunner()


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
    assert "export" in result.stdout.lower()
    assert "--app" in result.stdout
