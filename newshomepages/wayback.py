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
def single(handle: str) -> str:
    """Archive a URL."""
    # Pull the source’s metadata
    site = utils.get_site(handle)
    # Upload it
    wayback_url = _curl_url(site["url"])
    if wayback_url:
        click.echo(f"Archived {site['url']} at {wayback_url}")
    return wayback_url


@cli.command()
@click.argument("slug")
def bundle(slug: str) -> list:
    """Archive a bundle of sources."""
    site_list = utils.get_sites_in_bundle(slug)
    url_list = []
    for site in site_list:
        # Upload
        wayback_url = _curl_url(site["url"])
        time.sleep(2.5)
        if wayback_url:
            url_list.append([site["handle"], wayback_url])
    return url_list


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
