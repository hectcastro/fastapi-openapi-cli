import json
from pathlib import Path

import yaml
from fastapi import FastAPI


def get_openapi_spec(app: FastAPI) -> dict:
    return app.openapi()


def export_openapi(app: FastAPI, output_path: str | None) -> None:
    spec = get_openapi_spec(app)

    if output_path is None:
        print(json.dumps(spec, indent=2))
        return

    output_file = Path(output_path)

    if output_file.suffix in {".yaml", ".yml"}:
        with output_file.open("w") as f:
            yaml.safe_dump(spec, f, sort_keys=False)
    else:
        with output_file.open("w") as f:
            json.dump(spec, f, indent=2)
