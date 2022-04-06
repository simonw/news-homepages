import logging
import subprocess
import tempfile
from pathlib import Path

import click
import yaml
from playwright.sync_api import sync_playwright

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
    site = utils.get_site(handle)

    # Set the output path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        extension_path = utils.EXTENSIONS_PATH / "uBlock0.chromium"
        context = playwright.chromium.launch_persistent_context(
            tempfile.mkdtemp(),
            headless=False,
            args=[
                f"--disable-extensions-except={extension_path}",
                f"--load-extension={extension_path}",
            ],
        )
        print(context)
        page = context.background_pages[0]
        page.goto(site["url"])
        # Test the background page as you would any other page.
        context.close()


#    # Shoot the shot
#    command_list: typing.List[typing.Any] = [
#        "shot-scraper",
#        site["url"],
#        "-o",
#        str(output_path / f"{site['handle'].lower()}.jpg"),
#        "--quality",
#        "80",
#        "--width",
#        site["width"] or DEFAULT_WIDTH,
#        "--height",
#        site["height"] or DEFAULT_HEIGHT,
#        "--wait",
#        site["wait"] or DEFAULT_WAIT,
#        "--browser",
#        "chrome",
#        "--timeout",
#        str(60 * 1000),
#    ]
#    javascript = utils.get_javascript(site["handle"])
#    if javascript:
#        command_list.extend(["--javascript", javascript])
#    click.echo(f"Shooting {site['url']}")
#    subprocess.run(command_list)


@cli.command()
@click.argument("slug")
@click.option("-o", "--output-dir", "output_dir", default="./")
def bundle(slug: str, output_dir: str):
    """Screenshot a bundle of sources."""
    # Pull the source metadata
    site_list = utils.get_sites_in_bundle(slug)

    # Set the output path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Loop through the targets
    options_list = []
    for site in site_list:
        # Set the options for each
        site_options = dict(
            url=site["url"],
            output=str((output_path / f"{site['handle'].lower()}.jpg").absolute()),
            width=int(site["width"] or DEFAULT_WIDTH),
            height=int(site["height"] or DEFAULT_HEIGHT),
            quality=80,
            wait=int(site["wait"] or DEFAULT_WAIT),
        )
        javascript = utils.get_javascript(site["handle"])
        if javascript:
            site_options["javascript"] = javascript
        options_list.append(site_options)

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
        "--timeout",
        str(60 * 1000),
    ]
    click.echo(f"Shooting bundle with {yaml_path} configuration")
    subprocess.run(command_list)


if __name__ == "__main__":
    cli()
