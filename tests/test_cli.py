import json
from pathlib import Path

import pytest
import yaml

from fastapi_openapi_cli.cli import main


def test_export_to_stdout(capsys):
    exit_code = main(["--app", "tests.fixtures.sample_app:app"])
    captured = capsys.readouterr()

    assert exit_code == 0
    spec = json.loads(captured.out)
    assert spec["info"]["title"] == "Sample API"


def test_export_to_json_file(tmp_path: Path):
    output_file = tmp_path / "spec.json"
    exit_code = main(["--app", "tests.fixtures.sample_app:app", "-o", str(output_file)])

    assert exit_code == 0
    assert output_file.exists()

    with output_file.open() as f:
        spec = json.load(f)

    assert spec["info"]["title"] == "Sample API"


def test_export_to_yaml_file(tmp_path: Path):
    output_file = tmp_path / "spec.yaml"
    exit_code = main(["--app", "tests.fixtures.sample_app:app", "-o", str(output_file)])

    assert exit_code == 0
    assert output_file.exists()

    with output_file.open() as f:
        spec = yaml.safe_load(f)

    assert spec["info"]["title"] == "Sample API"


def test_export_with_invalid_app_path(capsys):
    exit_code = main(["--app", "nonexistent.module:app"])
    captured = capsys.readouterr()

    assert exit_code != 0
    assert "Could not import module" in captured.err


def test_export_help(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0
    captured = capsys.readouterr()

    assert "--app" in captured.out


def test_export_without_args_shows_help(capsys):
    exit_code = main([])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "--app" in captured.out
