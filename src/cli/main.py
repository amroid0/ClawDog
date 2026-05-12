from pathlib import Path
from typing import Annotated
import typer
from rich.console import Console
from utils.settings import get_settings
from utils.config import Config

app = typer.Typer(
    name="claw-dog",
    help="your loyal Ai Assistant",
    no_args_is_help=True,
    add_completion=True,
)
console = Console()
settings = get_settings()


def workspace_callback(context: typer.Context, workspace: str):
    context.ensure_object(dict)
    workSpacePath = Path(workspace)
    context.obj["workspace"] = workSpacePath
    return workSpacePath


@app.callback()
def main(
    ctx: typer.Context,
    workspace: str = typer.Option(
        settings.workspace_path,
        "--workspace",
        "-w",
        help="path to workspace directory",
        callback=workspace_callback,
    ),
):
    workspacePath = ctx.obj["workspace"]
    config_file = workspacePath / settings.workspace_file_name
    if not config_file.exists():
        console.print(f"[yellow] No Config found at {config_file}[/yellow]")
        raise typer.Exit(1)

    try:
        config = Config.load(workspacePath, config_file)
        ctx.obj["config"] = config
        console.print(f"[green]{config_file}[/green]")
    except Exception as e:
        console.print(f"[red] failed to load config {e}[/red]")
        raise typer.Exit(1)


@app.command("chat")
def chat(
    context: typer.Context,
    agent_id: Annotated[
        str | None,
        typer.Option(
            "--agent",
            "-a",
            help="agent id to use to override default agent from config",
        ),
    ] = None,
):
    console.print(f"[green]{context.obj['config']}[/green]")


if __name__ == "__main__":
    app()
