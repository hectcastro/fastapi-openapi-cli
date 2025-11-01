import json
from pathlib import Path

import pytest
import yaml
from fastapi import FastAPI

from fastapi_openapi_cli.export import export_openapi


@pytest.fixture
def sample_app() -> FastAPI:
    app = FastAPI(title="Test API", version="1.0.0", description="A test API")

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    return app


def test_get_openapi_spec(sample_app: FastAPI):
    from fastapi_openapi_cli.export import get_openapi_spec

    spec = get_openapi_spec(sample_app)

    assert isinstance(spec, dict)
    assert spec["info"]["title"] == "Test API"
    assert spec["info"]["version"] == "1.0.0"
    assert "/health" in spec["paths"]


def test_export_to_json_file(sample_app: FastAPI, tmp_path: Path):
    output_file = tmp_path / "openapi.json"

    export_openapi(sample_app, str(output_file))

    assert output_file.exists()
    with output_file.open() as f:
        spec = json.load(f)

    assert spec["info"]["title"] == "Test API"
    assert spec["info"]["version"] == "1.0.0"


def test_export_to_yaml_file(sample_app: FastAPI, tmp_path: Path):
    output_file = tmp_path / "openapi.yaml"

    export_openapi(sample_app, str(output_file))

    assert output_file.exists()
    with output_file.open() as f:
        spec = yaml.safe_load(f)

    assert spec["info"]["title"] == "Test API"
    assert spec["info"]["version"] == "1.0.0"


def test_export_to_stdout_defaults_to_json(sample_app: FastAPI, capsys):
    export_openapi(sample_app, None)

    captured = capsys.readouterr()
    spec = json.loads(captured.out)

    assert spec["info"]["title"] == "Test API"
