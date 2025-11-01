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


def test_load_app_with_missing_attribute():
    with pytest.raises(AppLoadError, match="Module .* has no attribute"):
        load_app("tests.fixtures.no_app:app")


def test_load_app_with_non_fastapi_instance():
    with pytest.raises(AppLoadError, match="is not a FastAPI instance"):
        load_app("tests.fixtures.wrong_type:app")
