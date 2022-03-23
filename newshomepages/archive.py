import os
from datetime import datetime
from pathlib import Path

import click
import internetarchive
import pytz

from . import utils

IA_ACCESS_KEY = os.getenv("IA_ACCESS_KEY")
IA_SECRET_KEY = os.getenv("IA_SECRET_KEY")
IA_COLLECTION = os.getenv("IA_COLLECTION")


@click.group()
def cli():
    """Shoot a screenshot."""
    pass


@cli.command()
@click.argument("handle")
@click.option("-i", "--input-dir", "input_dir", default="./")
def single(handle, input_dir):
    """Archive a screenshot."""
    # Pull the source’s metadata
    data = utils.get_site(handle)
    # Upload it
    _upload(data, input_dir)


@cli.command()
@click.argument("slug")
@click.option("-i", "--input-dir", "input_dir", default="./")
def bundle(slug, input_dir):
    """Send a bundle of sources."""
    bundle = utils.get_bundle(slug)
    handle_list = [
        h["handle"] for h in utils.get_site_list() if h["bundle"] == bundle["slug"]
    ]
    for handle in handle_list:
        # Pull the source’s metadata
        data = utils.get_site(handle)
        # Upload
        _upload(data, input_dir)


def _upload(data, input_dir):
    # Set the input path
    input_path = Path(input_dir).absolute()
    image_path = input_path / f"{data['handle']}.jpg"

    # Get the timestamp
    now = datetime.now()

    # Convert it to local time
    tz = pytz.timezone(data["timezone"])
    now_local = now.astimezone(tz)

    # We will post the file into an "item" keyed to the site's handle and year
    identifier = f"{data['handle'].lower()}-{now_local.strftime('%Y')}"
    kwargs = dict(
        # Authentication
        access_key=IA_ACCESS_KEY,
        secret_key=IA_SECRET_KEY,
        # Metadata about the item
        metadata=dict(
            title=f"{data['name']} homepages in {now_local.strftime('%Y')}",
            collection=IA_COLLECTION,
            mediatype="image",
            publisher=data["url"],
            date=now_local.strftime("%Y"),
            contributor="https://github.com/palewire/news-homepages",
        ),
        # Metadata about the image file
        files={f"{data['handle']}-{now_local.isoformat()}.jpg": image_path},
    )

    # Upload it
    internetarchive.upload(identifier, **kwargs)


if __name__ == "__main__":
    cli()
