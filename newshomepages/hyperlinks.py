import json
import logging
import time
from pathlib import Path

import click
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

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
    """Save all hyperlinsk as JSON for a single site."""
    # Get metadata
    data = utils.get_site(handle)

    # Set the output path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Do it
    _get_links(data, output_path)


@cli.command()
@click.argument("slug")
@click.option("-o", "--output-dir", "output_dir", default="./")
def bundle(slug: str, output_dir: str):
    """Save all hyperlinks as JSON for a bundle of sites."""
    # Pull the source metadata
    bundle = utils.get_bundle(slug)
    handle_list = [h for h in utils.get_site_list() if h["bundle"] == bundle["slug"]]

    # Set the output path
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Loop through the targets
    for handle in handle_list:
        # Set the options for each
        _get_links(handle, output_path)
        time.sleep(0.25)


def _get_links(data, output_path):
    click.echo(f"Getting hyperlinks for {data['url']}")
    # Start the browser
    with sync_playwright() as p:
        browser_obj = p.chromium.launch()
        # Get the page
        page = browser_obj.new_page()
        page.goto(data["url"])

        # Pull the html
        html = page.content()

        # Parse out all the links
        soup = BeautifulSoup(html, "html5lib")
        link_list = soup.find_all("a")

        # Close the browser
        browser_obj.close()

    # Parse out the data we want to keep
    data_list = []
    for link in link_list:
        try:
            d = {
                "text": link.text,
                "url": link["href"],
            }
        except KeyError:
            # If no href, skip it
            continue

        # Add to big list
        data_list.append(d)

    # Write it out
    with open(output_path / f"{data['handle']}.hyperlinks.json", "w") as fp:
        json.dump(data_list, fp, indent=2)


if __name__ == "__main__":
    cli()
