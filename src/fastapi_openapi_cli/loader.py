import importlib
from typing import Any

from fastapi import FastAPI


def load_app(app_path: str) -> FastAPI:
    module_path, app_name = app_path.split(":")
    module = importlib.import_module(module_path)
    app: Any = getattr(module, app_name)
    return app
