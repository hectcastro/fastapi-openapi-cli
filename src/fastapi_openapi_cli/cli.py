import argparse
import sys
from collections.abc import Sequence

from fastapi_openapi_cli.export import export_openapi
from fastapi_openapi_cli.loader import AppLoadError, load_app


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fastapi-openapi",
        description="CLI tool to export FastAPI OpenAPI specifications",
    )
    parser.add_argument(
        "--app",
        "-a",
        required=True,
        help="FastAPI app path (e.g., module:app)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output file path (default: stdout)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    arguments = list(argv) if argv is not None else sys.argv[1:]

    if not arguments:
        parser.print_help()
        return 0

    args = parser.parse_args(arguments)

    try:
        fastapi_app = load_app(args.app)
        export_openapi(fastapi_app, args.output)
    except AppLoadError as e:
        print(str(e), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
