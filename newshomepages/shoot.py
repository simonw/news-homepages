import logging
import subprocess
from pathlib import Path

import click

from . import utils

DEFAULT_WIDTH = "1300"
DEFAULT_HEIGHT = "1600"
DEFAULT_WAIT = "2000"

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
    data = utils.get_site(handle)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    _shoot(
        data["url"],
        output_path / f"{data['handle']}.jpg",
        data["width"] or DEFAULT_WIDTH,
        data["height"] or DEFAULT_HEIGHT,
        data["wait"] or DEFAULT_WAIT,
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
        )


def _shoot(url, output, width, height, wait):
    logger.debug(f"Shooting {url}")
    subprocess.run(
        [
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
    )


if __name__ == "__main__":
    cli()
