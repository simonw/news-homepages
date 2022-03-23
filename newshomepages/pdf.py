import logging
import subprocess
from pathlib import Path

import click

from . import utils

DEFAULT_WAIT = "3000"

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Shoot a screenshot."""
    pass


@cli.command()
@click.argument("handle")
@click.option("-o", "--output-dir", "output_dir", default="./")
def single(handle, output_dir):
    """Save a single source as a full-page PDF."""
    # Get metadata
    data = utils.get_site(handle)

    # Set the output path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Shoot the shot
    command_list = [
        "shot-scraper",
        "pdf",
        data["url"],
        "-o",
        output_path / f"{data['handle']}.pdf",
        "--wait",
        data["wait"] or DEFAULT_WAIT,
    ]
    javascript = utils.get_javascript(data["handle"])
    if javascript:
        command_list.extend(["--javascript", javascript])
    click.echo(f"Shooting {data['url']}")
    subprocess.run(command_list)


if __name__ == "__main__":
    cli()
