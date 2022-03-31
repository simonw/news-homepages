import time

import click
import savepagenow
from savepagenow.exceptions import CachedPage, TooManyRequests

from . import utils


@click.group()
def cli():
    """Shoot a screenshot."""
    pass


@cli.command()
@click.argument("handle")
def single(handle: str) -> str:
    """Archive a URL."""
    # Pull the source’s metadata
    data = utils.get_site(handle)
    # Upload it
    wayback_url = _save_url(data["url"])
    if wayback_url:
        click.echo(f"Archived {data['url']} at {wayback_url}")
    return wayback_url


@cli.command()
@click.argument("slug")
def bundle(slug: str) -> list:
    """Archive a bundle of sources."""
    bundle = utils.get_bundle(slug)
    handle_list = [
        h["handle"] for h in utils.get_site_list() if h["bundle"] == bundle["slug"]
    ]
    url_list = []
    for handle in handle_list:
        # Pull the source’s metadata
        data = utils.get_site(handle)
        # Upload
        wayback_url = _save_url(data["url"])
        time.sleep(2.5)
        if wayback_url:
            url_list.append([data["handle"], wayback_url])
    return url_list


def _save_url(url):
    try:
        return savepagenow.capture(
            url,
            user_agent="news-homepages (https://palewi.re/docs/savepagenow/)",
        )
    except CachedPage:
        click.echo(f"archive.org returned a recent cache for {url}")
        return None
    except TooManyRequests:
        click.echo(f"archive.org has already archived {url} 10 times today")
        return None


if __name__ == "__main__":
    cli()
