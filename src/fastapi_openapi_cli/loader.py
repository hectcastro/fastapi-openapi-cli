import importlib
from typing import Any

from fastapi import FastAPI


class AppLoadError(Exception):
    pass


def load_app(app_path: str) -> FastAPI:
    module_path, app_name = app_path.split(":")

    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as e:
        raise AppLoadError(f"Could not import module '{module_path}': {e}") from e

    app: Any = getattr(module, app_name)
    return app
