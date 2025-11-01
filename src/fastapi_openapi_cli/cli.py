import typer

from fastapi_openapi_cli.export import export_openapi
from fastapi_openapi_cli.loader import AppLoadError, load_app

app = typer.Typer(
    name="fastapi-openapi",
    help="CLI tool to export FastAPI OpenAPI specifications",
    no_args_is_help=True,
)


@app.command()
def export(
    app_path: str = typer.Option(..., "--app", "-a", help="FastAPI app path (e.g., module:app)"),
    output: str | None = typer.Option(
        None, "--output", "-o", help="Output file path (default: stdout)"
    ),
) -> None:
    """
    Export the OpenAPI specification from a FastAPI application.

    Supports both JSON and YAML formats. Format is auto-detected from file extension.
    If no output file is specified, outputs JSON to stdout.
    """
    try:
        fastapi_app = load_app(app_path)
        export_openapi(fastapi_app, output)
    except AppLoadError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(code=1) from e
