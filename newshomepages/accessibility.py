import logging
import subprocess
import time
import typing
from pathlib import Path

import click

from . import utils

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Save an accessibility JSON."""
    pass


@cli.command()
@click.argument("handle")
@click.option("-o", "--output-dir", "output_dir", default="./")
def single(handle: str, output_dir: str):
    """Save the accessiblity JSON of a single site."""
    # Get metadata
    data = utils.get_site(handle)

    # Set the output path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Do the thing
    _get_accessibility(data, output_path)


@cli.command()
@click.argument("slug")
@click.option("-o", "--output-dir", "output_dir", default="./")
def bundle(slug: str, output_dir: str):
    """Save the accessibility JSON of a bundle of sites."""
    # Pull the source metadata
    bundle = utils.get_bundle(slug)
    handle_list = [h for h in utils.get_site_list() if h["bundle"] == bundle["slug"]]

    # Set the output path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Loop through the targets
    for handle in handle_list:
        # Set the options for each
        _get_accessibility(handle, output_path)
        time.sleep(0.25)


def _get_accessibility(data, output_path):
    # Shoot the shot
    command_list: typing.List[typing.Any] = [
        "shot-scraper",
        "accessibility",
        data["url"],
        "-o",
        str(output_path / f"{data['handle']}.json"),
    ]
    javascript = utils.get_javascript(data["handle"])
    if javascript:
        command_list.extend(["--javascript", javascript])
    click.echo(f"Parsing {data['url']}")
    subprocess.run(command_list)


if __name__ == "__main__":
    cli()
