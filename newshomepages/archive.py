import os
from datetime import datetime

import click
import internetarchive
from pathlib import Path
import pytz

from . import utils

IA_ACCESS_KEY = os.getenv("IA_ACCESS_KEY")
IA_SECRET_KEY = os.getenv("IA_SECRET_KEY")
IA_COLLECTION = os.getenv("IA_COLLECTION")


@click.command()
@click.argument("handle")
@click.option("-i", "--input-dir", "input_dir", default="./")
def cli(handle, input_dir):
    """Archive a screenshot."""
    # Pull the source’s metadata
    data = utils.get_site(handle)

    # Set the input path
    input_path = Path(input_dir).absolute()
    image_path = input_path / f"{data['handle']}.jpg"

    # Get the timestamp
    now = datetime.now()

    # Convert it to local time
    tz = pytz.timezone(data["timezone"])
    now_local = now.astimezone(tz)

    # We will post the file into an "item" keyed to the site's handle and year
    identifier = f"{handle.lower()}-{now_local.strftime('%Y')}"
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
            date=now_local.strftime('%Y'),
            contributor="https://github.com/palewire/news-homepages",
        ),
        # Metadata about the image file
        files={f"{data['handle']}-{now_local.isoformat()}.jpg": image_path},
    )

    # Upload it
    internetarchive.upload(identifier, **kwargs)


if __name__ == "__main__":
    cli()
