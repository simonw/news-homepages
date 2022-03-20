import logging
import subprocess
from pathlib import Path

import click

from . import utils

DEFAULT_WIDTH = "1300"
DEFAULT_HEIGHT = "1600"
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
    """Screenshot a single source."""
    # Get metadata
    data = utils.get_site(handle)

    # Set the output path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Shoot the shot
    _shoot(
        data["url"],
        output_path / f"{data['handle']}.jpg",
        data["width"] or DEFAULT_WIDTH,
        data["height"] or DEFAULT_HEIGHT,
        data["wait"] or DEFAULT_WAIT,
        javascript=utils.get_javascript(data["handle"]),
    )


@cli.command()
@click.argument("slug")
@click.option("-o", "--output-dir", "output_dir", default="./")
def bundle(slug, output_dir):
    """Screenshot a bundle of sources."""
    # Pull the source metadata
    bundle = utils.get_bundle(slug)
    target_list = [h for h in utils.get_site_list() if h["bundle"] == bundle["slug"]]

    # Set the output path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Loop through the targets
    for target in target_list:
        # Shoot them one by one
        _shoot(
            target["url"],
            output_path / f"{target['handle']}.jpg",
            target["width"] or DEFAULT_WIDTH,
            target["height"] or DEFAULT_HEIGHT,
            target["wait"] or DEFAULT_WAIT,
            javascript=utils.get_javascript(target["handle"]),
        )


def _shoot(url, output, width, height, wait, javascript=None):
    click.echo(f"Shooting {url}")
    command_list = [
        "shot-scraper",
        url,
        "-o",
        output,
        "--quality",
        "80",
        "--width",
        width,
        "--height",
        height,
        "--wait",
        wait,
    ]
    if javascript:
        command_list.extend(["--javascript", javascript])
    subprocess.run(command_list)


if __name__ == "__main__":
    cli()
