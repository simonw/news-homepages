import os
import time
import typing

import click
import savepagenow
from savepagenow.exceptions import CachedPage, TooManyRequests, UnknownError

from . import utils

IA_ACCESS_KEY = os.getenv("IA_ACCESS_KEY")
IA_SECRET_KEY = os.getenv("IA_SECRET_KEY")


@click.group()
def cli():
    """Shoot a screenshot."""
    pass


@cli.command()
@click.argument("handle")
def single(handle: str):
    """Archive a URL."""
    # Pull the source’s metadata
    site = utils.get_site(handle)
    # Upload it
    _curl_url(site["url"])


@cli.command()
@click.argument("slug")
def bundle(slug: str):
    """Archive a bundle of sources."""
    site_list = utils.get_sites_in_bundle(slug)
    for site in site_list:
        # Upload
        _curl_url(site["url"])
        time.sleep(2.5)


def _curl_url(url):
    command_list: typing.List[str] = [
        "curl",
        "-X",
        "POST",
        "-H",
        "'Accept: application/json'",
        "-H",
        f"'Authorization: LOW {IA_ACCESS_KEY}:{IA_SECRET_KEY}'",
        "-d",
        f"'url={url}'",
        "https://web.archive.org/save",
    ]
    click.echo(f"Archiving {url}\n")
    os.system(" ".join(command_list))


if __name__ == "__main__":
    cli()
