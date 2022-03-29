import logging
import subprocess
import tempfile
import typing
from pathlib import Path

import click
import yaml

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
def single(handle: str, output_dir: str):
    """Screenshot a single source."""
    # Get metadata
    data = utils.get_site(handle)

    # Set the output path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Shoot the shot
    command_list: typing.List[typing.Any] = [
        "shot-scraper",
        data["url"],
        "-o",
        str(output_path / f"{data['handle']}.jpg"),
        "--quality",
        "80",
        "--width",
        data["width"] or DEFAULT_WIDTH,
        "--height",
        data["height"] or DEFAULT_HEIGHT,
        "--wait",
        data["wait"] or DEFAULT_WAIT,
        "--browser",
        "chrome",
    ]
    javascript = utils.get_javascript(data["handle"])
    if javascript:
        command_list.extend(["--javascript", javascript])
    click.echo(f"Shooting {data['url']}")
    subprocess.run(command_list)


@cli.command()
@click.argument("slug")
@click.option("-o", "--output-dir", "output_dir", default="./")
def bundle(slug: str, output_dir: str):
    """Screenshot a bundle of sources."""
    # Pull the source metadata
    bundle = utils.get_bundle(slug)
    handle_list = [h for h in utils.get_site_list() if h["bundle"] == bundle["slug"]]

    # Set the output path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Loop through the targets
    options_list = []
    for handle in handle_list:
        # Set the options for each
        handle_options = dict(
            url=handle["url"],
            output=str((output_path / f"{handle['handle']}.jpg").absolute()),
            width=int(handle["width"] or DEFAULT_WIDTH),
            height=int(handle["height"] or DEFAULT_HEIGHT),
            quality=80,
            wait=int(handle["wait"] or DEFAULT_WAIT),
        )
        javascript = utils.get_javascript(handle["handle"])
        if javascript:
            handle_options["javascript"] = javascript
        options_list.append(handle_options)

    # Write out YAML config file
    yaml_str = yaml.dump(options_list)
    with tempfile.NamedTemporaryFile(suffix=".yml", delete=False) as fh:
        fh.write(bytes(yaml_str, "utf-8"))
        yaml_path = Path(fh.name)

    # Shoot
    command_list = [
        "shot-scraper",
        "multi",
        str(yaml_path),
        "--browser",
        "chrome",
    ]
    click.echo(f"Shooting bundle with {yaml_path} configuration")
    subprocess.run(command_list)


if __name__ == "__main__":
    cli()
