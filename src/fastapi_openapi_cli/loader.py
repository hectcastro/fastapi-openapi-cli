import importlib

from fastapi import FastAPI


class AppLoadError(Exception):
    pass


def load_app(app_path: str) -> FastAPI:
    module_path, app_name = app_path.split(":")

    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as e:
        raise AppLoadError(f"Could not import module '{module_path}': {e}") from e

    try:
        app = getattr(module, app_name)
    except AttributeError as e:
        raise AppLoadError(f"Module '{module_path}' has no attribute '{app_name}'") from e

    if not isinstance(app, FastAPI):
        raise AppLoadError(
            f"Attribute '{app_name}' in module '{module_path}' is not a FastAPI instance"
        )

    return app
