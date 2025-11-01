import pytest
from fastapi import FastAPI

from fastapi_openapi_cli.loader import AppLoadError, load_app


def test_load_app_with_valid_module_path():
    app = load_app("tests.fixtures.sample_app:app")

    assert isinstance(app, FastAPI)
    assert app.title == "Sample API"
    assert app.version == "1.0.0"


def test_load_app_with_invalid_module_path():
    with pytest.raises(AppLoadError, match="Could not import module"):
        load_app("nonexistent.module:app")
